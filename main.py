import atoti as tt
import setup
import utils


utils.log_event("Launching Atoti CPR")
config = utils.execute(tt.config.create_config, {'port': 9009}, event_name="Session configuration")

session = utils.execute(tt.create_session, {'config': config}, event_name="Session creation")

session.load_all_data()

utils.log_event("Initialising Atoti...")
utils.execute(setup.init_cube, {'session': session}, "Atoti launch")

utils.log_event("Instance available at " + session.url)

session.wait()
