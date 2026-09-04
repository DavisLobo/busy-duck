from sqlalchemy.orm import Session

from busy_duck.database.models.provider_model import ProviderModel


class ProviderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, provider: ProviderModel) -> ProviderModel:
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return provider

    def find_by_id(self, provider_id: str) -> ProviderModel | None:
        return self.session.query(ProviderModel).filter(ProviderModel.id == provider_id).first()

    def find_by_slug(self, slug: str) -> ProviderModel | None:
        return self.session.query(ProviderModel).filter(ProviderModel.slug == slug).first()