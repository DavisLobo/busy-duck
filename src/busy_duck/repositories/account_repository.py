from sqlalchemy.orm import Session

from busy_duck.database.models.account_model import AccountModel


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, account: AccountModel) -> AccountModel:
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def find_by_id(self, account_id: str) -> AccountModel | None:
        return self.session.query(AccountModel).filter(AccountModel.id == account_id).first()

    def find_by_email(self, email: str) -> AccountModel | None:
        return self.session.query(AccountModel).filter(AccountModel.email == email).first()

    def find_by_provider_id(self, provider_id: str) -> list[AccountModel]:
        return (
            self.session.query(AccountModel)
            .filter(AccountModel.provider_id == provider_id)
            .all()
        )

    def find_active(self) -> list[AccountModel]:
        return (
            self.session.query(AccountModel)
            .filter(AccountModel.is_active.is_(True))
            .all()
        )

    def find_all(self) -> list[AccountModel]:
        return self.session.query(AccountModel).all()

    def delete(self, account: AccountModel) -> None:
        self.session.delete(account)
        self.session.commit()