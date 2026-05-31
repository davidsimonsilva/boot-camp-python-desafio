from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager

import models
import schemas
import security
from database import init_db
from dependencies import get_db, get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco de dados em memória no startup
    await init_db()
    yield

app = FastAPI(
    title="Async Banking API",
    description="API Bancária Assíncrona com suporte a transações e autenticação JWT.",
    version="1.0.0",
    lifespan=lifespan
)

# --- ROTAS DE AUTENTICAÇÃO E USUÁRIO ---

@app.post("/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Autenticação"])
async def register(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Cria uma nova conta corrente no sistema."""
    result = await db.execute(select(models.User).where(models.User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username já está em uso.")
    
    hashed_password = security.get_password_hash(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=schemas.Token, tags=["Autenticação"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Autentica o usuário e retorna o Token JWT."""
    result = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos.")
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- ROTAS BANCÁRIAS (PROTEGIDAS) ---

@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED, tags=["Operações Bancárias"])
async def create_transaction(
    transaction_data: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Registra uma transação (Depósito ou Saque) na conta do usuário autenticado.
    Valida se há saldo suficiente em caso de saques.
    """
    if transaction_data.type == models.TransactionType.DEPOSIT:
        current_user.balance += transaction_data.amount
        
    elif transaction_data.type == models.TransactionType.WITHDRAW:
        if current_user.balance < transaction_data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Saldo insuficiente para realizar o saque."
            )
        current_user.balance -= transaction_data.amount

    new_transaction = models.Transaction(
        account_id=current_user.id,
        type=transaction_data.type,
        amount=transaction_data.amount
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

@app.get("/statement", response_model=schemas.StatementResponse, tags=["Operações Bancárias"])
async def get_statement(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retorna o saldo atual e o histórico completo de transações do usuário."""
    # Recarrega o usuário trazendo junto as transações de forma assíncrona
    result = await db.execute(
        select(models.User)
        .where(models.User.id == current_user.id)
        .options(selectinload(models.User.transactions))
    )
    user_with_transactions = result.scalar_one()
    
    return {
        "balance": user_with_transactions.balance,
        "transactions": user_with_transactions.transactions
    }
