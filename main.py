import atoti as tt
import setup

config = tt.config.create_config(port=9009)
session = tt.create_session(config=config)
session.load_all_data()

setup.init_cube(session=session)

print(session.url)

session.wait()
