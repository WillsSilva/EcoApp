from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, expenses, income, goals, category, auth

# Cria as tabelas no banco (temporário, ideal é usar Alembic depois)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui as rotas
app.include_router(user.router)
app.include_router(expenses.router)
app.include_router(income.router)
app.include_router(goals.router)
app.include_router(category.router)
app.include_router(auth.router)
