from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)

    # Establishes relationship to child model; back_populates keeps both sides synced
    logs = relationship("ExecutionLog", back_populates="user", cascade="all, delete-orphan")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign Key reference

    user = relationship("User", back_populates="logs")


# --- Usage Example ---
engine = create_engine("postgresql://postgres:postgres@localhost:5432/dataops_db")
SessionLocal = sessionmaker(bind=engine)

def fetch_user_logs(username: str):
    with SessionLocal() as session:
        # Join tables explicitly using the ORM relationship
        results = (
            session.query(ExecutionLog)
            .join(User)
            .filter(User.username == username, ExecutionLog.status == "FAILED")
            .all()
        )
        return results


import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Pipeline(Base):
    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)


# Async connection string requires postgresql+asyncpg://
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/dataops_db"

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Factory for creating async sessions
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_active_pipelines_async() -> list[Pipeline]:
    async with AsyncSessionLocal() as session:
        # SQLAlchemy 2.0 style uses select() constructs instead of session.query()
        stmt = select(Pipeline).where(Pipeline.active == True)
        
        # Await execution asynchronously
        result = await session.execute(stmt)
        
        # .scalars() extracts ORM objects directly from result rows
        pipelines = result.scalars().all()
        return list(pipelines)

# Run loop: asyncio.run(get_active_pipelines_async())