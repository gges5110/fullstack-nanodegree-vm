from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Base, Item

engine = create_engine('sqlite:///catalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#Menu for UrbanBurger
catalog1 = Catalog(name = "Snowboarding")
session.add(catalog1)
session.commit()

menuItem1 = Item(title = "Snowboard", description = "with garlic and parmesan",
        price = "2.99", catalog = catalog1, user_id=2, picture="https://i.ytimg.com/vi/Zl6xwuBJVIY/maxresdefault.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = Item(title = "Goggles", description = "with garlic and parmesan",
        price = "3.99", catalog = catalog1, user_id=2, picture="https://i.ytimg.com/vi/Zl6xwuBJVIY/maxresdefault.jpg")
session.add(menuItem2)
session.commit()

catalog2 = Catalog(name = "Soccer")
session.add(catalog2)
session.commit()

menuItem3 = Item(title = "Soccer ball", description = "with garlic and parmesan",
        price = "4.99", catalog = catalog2, user_id=1, picture="https://i.ytimg.com/vi/Zl6xwuBJVIY/maxresdefault.jpg")
session.add(menuItem3)
session.commit()

catalog3 = Catalog(name = "Basketball")
session.add(catalog3)
session.commit()

catalog4 = Catalog(name = "Frisbee")
session.add(catalog4)
session.commit()

catalog5 = Catalog(name = "Rock Climbing")
session.add(catalog5)
session.commit()
print "added catalog items!"
