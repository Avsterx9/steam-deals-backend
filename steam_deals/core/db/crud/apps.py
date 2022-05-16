from sqlalchemy.orm import Session

from steam_deals.core import models
from steam_deals.core import schemas


def create_app(db: Session, app: schemas.AppBase) -> models.App:
    db_app = models.App(
        steam_appid=app.steam_appid,
        name=app.name,
        header_image=app.header_image,
        developers=', '.join(map(str, app.developers)),
        publishers=', '.join(map(str, app.publishers)),
        price=app.price.final,
    )

    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_app_by_app_id(db: Session, app_id: int) -> models.App:
    return db.query(models.App).get(app_id)
