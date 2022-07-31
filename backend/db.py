# (C) 2022 Debonair Demons
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from uuid import uuid4
from tinydb import TinyDB, Query
import datetime
import os

if not os.path.isdir("./data"):
    os.makedirs("./data")
if not os.path.isdir("./documents"):
    os.makedirs("./documents")


class DatabaseHandler:
    def __init__(self):
        self.db = TinyDB("./data/db.json")
        self.generated_ids = self.db.table("generated_ids")
        self.users = self.db.table("users")
        self.documents = self.db.table("documents")

    async def generate_id(self):
        new_id = uuid4().__str__()
        while self.generated_ids.contains(Query()["id"] == new_id.__str__()):
            new_id = uuid4()
        self.generated_ids.insert({"id": new_id.__str__()})
        self.db.close()
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

        new_user = {
            "id": user_id,
            "username": username,
            "password": password,
            "salt": salt,
            "creation_date": creation_date,
            "char_count": [10] * 62,
            "score": 0,
        }

        self.users.insert(new_user)
        self.db.close()
        return new_user

    async def create_document(self, user_id: str, doc_name: str) -> bool:
        if not doc_name:
            raise AttributeError(
                '"doc_name" parameter not found when creating document!'
            )
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')

        doc_id = await self.generate_id()
        creation_date = datetime.datetime.now()

        # Create the file
        open(f"./documents/{doc_id}-{doc_name}-{creation_date.isoformat()}.md", "w")

        new_doc = {
            "id": doc_id,
            "name": doc_name,
            "creation_date": creation_date,
            "owner_id": user_id,
            "path": f"./documents/{doc_id}-{doc_name}-{creation_date.isoformat()}.md",
        }

        self.documents.insert(new_doc)
        self.db.close()
        return new_doc

    async def get_user(self, user_id: str) -> dict:
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        self.db.close()
        return self.users.search(Query()["id"] == user_id)[0]

    async def get_document(self, doc_id: str) -> dict:
        check_doc = self.documents.contains(Query()["id"] == doc_id)
        if not check_doc:
            raise ValueError('"doc_id" not found in database!')
        self.db.close()
        return self.documents.search(Query()["id"] == doc_id)[0]

    async def update_char_count(self, user_id: str, char_count: list):
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        self.users.update({"char_count": char_count}, Query()["id"] == user_id)
        self.db.close()
        
    async def update_score(self, user_id: str, score: int):
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        self.users.update({"score": score}, Query()["id"] == user_id)
        self.db.close()

    async def get_user_documents(self, user_id: str) -> list:
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        return self.documents.search(Query()["owner_id"] == user_id)

    async def update_document(self, doc_id: str, doc_name: str):
        check_doc = self.documents.contains(Query()["id"] == doc_id)
        if not check_doc:
            raise ValueError('"doc_id" not found in database!')
        self.documents.update({"name": doc_name}, Query()["id"] == doc_id)
        self.db.close()

    async def delete_document(self, doc_id: str):
        check_doc = self.documents.contains(Query()["id"] == doc_id)
        if not check_doc:
            raise ValueError('"doc_id" not found in database!')
        os.remove(self.documents.search(Query()["id"] == doc_id)[0]["path"])
        self.documents.remove(Query()["id"] == doc_id)
        self.db.close()

    async def delete_user(self, user_id: str):
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        self.users.remove(Query()["id"] == user_id)
        self.db.close()

    async def write_document(self, doc_id: str, text: str):
        check_doc = self.documents.contains(Query()["id"] == doc_id)
        if not check_doc:
            raise ValueError('"doc_id" not found in database!')
        with open(self.documents.search(Query()["id"] == doc_id)[0]["path"], "a") as f:
            # Append the text to the file
            f.write(text)
        file_len = open(self.documents.search(Query()["id"] == doc_id)[0]["path"], "r").read().__len__()
        return file_len

    async def read_document(self, doc_id: str) -> str:
        check_doc = self.documents.contains(Query()["id"] == doc_id)
        if not check_doc:
            raise ValueError('"doc_id" not found in database!')
        with open(self.documents.search(Query()["id"] == doc_id)[0]["path"], "r") as f:
            return f.read()
    
    async def get_char_count(self, user_id: str) -> list:
        check_user = self.users.contains(Query()["id"] == user_id)
        if not check_user:
            raise ValueError('"user_id" not found in database!')
        return self.users.search(Query()["id"] == user_id)[0]["char_count"]