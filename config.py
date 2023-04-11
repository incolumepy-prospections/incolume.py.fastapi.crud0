
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="INCOLUME",
    settings_files=['settings.toml', '.secrets.toml'],
    environments=['development', 'dev0', 'testing', 'production'],
    env_switcher='INCOLUME_MODE',
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
