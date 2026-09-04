from sqlalchemy.orm import Session

from busy_duck.database.models.provider_config_model import ProviderConfigModel


class ProviderConfigRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, config: ProviderConfigModel) -> ProviderConfigModel:
        self.session.add(config)
        self.session.commit()
        self.session.refresh(config)
        return config

    def find_by_provider_id(self, provider_id: str) -> ProviderConfigModel | None:
        return (
            self.session.query(ProviderConfigModel)
            .filter(ProviderConfigModel.provider_id == provider_id)
            .first()
        )