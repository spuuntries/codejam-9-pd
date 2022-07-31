# (C) 2022 Debonair Demons
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from uuid import uuid4
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime
import sqlalchemy
import os

if not os.path.isdir("./data"):
    os.makedirs("./data")
if not os.path.isdir("./documents"):
    os.makedirs("./documents")
metadata = sqlalchemy.MetaData()
Base = declarative_base()


class user_data(Base):
    __tablename__ = "user_data"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    salt = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(sqlalchemy.Date)
    char_count = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer, dimensions=1))
    score = sqlalchemy.Column(sqlalchemy.Float)

    documents_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("documents.id")
    )
    documents = relationship("documents", back_populates="user_data", uselist=True)


class documents(Base):
    __tablename__ = "documents"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    path = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(sqlalchemy.Date)

    owner_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("user_data.id")
    )
    owner = relationship("user_data", back_populates="documents", uselist=False)


class generated_ids(Base):
    __tablename__ = "generated_ids"

    ids = sqlalchemy.Column(sqlalchemy.String, primary_key=True)


engine = sqlalchemy.create_engine(
    f"sqlite:///./data/store.db", connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class DatabaseHandler:
    def __init__(self):
        self.generated_ids = []

    async def generate_id(self):
        new_id = uuid4()
        while new_id in self.generated_ids:
            new_id = uuid4()
        self.generated_ids.append(new_id)
        return new_id

    async def create_user(self, username: str, password: str, salt: str):
        if not username:
            raise AttributeError('"username" parameter not found when creating user!')
        if not password:
            raise AttributeError('"password" parameter not found when creating user!')
        if not salt:
            raise AttributeError('"salt" parameter not found when creating user!')

        user_id = await self.generate_id()
        creation_date = datetime.datetime.now()

        new_user = user_data(
            id=user_id,
            username=username,
            password=password,
            salt=salt,
            creation_date=creation_date,
            char_count=[10] * 36,
            score=0,
        )

        session.add(new_user)
        session.commit()
        return new_user

    async def create_document(self, user_id: str, doc_name: str) -> bool:
        if not doc_name:
            raise AttributeError(
                '"doc_name" parameter not found when creating document!'
            )
        check_user = session.query(user_data).filter(user_data.id == user_id).count()
        if check_user < 1:
            raise ValueError('"user_id" not found in database!')

        doc_id = await self.generate_id()
        creation_date = datetime.datetime.now()

        # Create the file
        open(f"./documents/{doc_id}-{doc_name}-{creation_date.isoformat()}.md", "w")

        new_doc = documents(
            id=doc_id,
            owner_id=user_id,
            name=doc_name,
            path=f"./documents/{doc_id}-{doc_name}-{creation_date.isoformat()}.md",
            creation_date=creation_date,
        )

        session.add(new_doc)
        session.commit()
        return new_doc
