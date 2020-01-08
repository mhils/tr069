import code
import platform
from typing import Sequence

import click

import tr069

try:
    import readline
except ImportError:
    pass


class TR069Console(code.InteractiveConsole):
    def __init__(self, commands: Sequence[str] = ()):
        self.commands = list(commands)
        super().__init__()

    def raw_input(self, prompt=""):
        # https://github.com/pallets/click/issues/665
        # click.style does not work with input()
        if platform.system() != "Windows":  # pragma: no cover
            prompt = click.style(prompt, fg="yellow", bold=True)
        if self.commands:
            command = self.commands.pop(0)
            click.echo(f"{prompt}{command}")
            return command
        else:
            # https://github.com/pallets/click/issues/665
            # return click.prompt(prompt, prompt_suffix="")
            return input(prompt)


@click.command()
@click.argument("acs-url")
@click.option('-b', '--basic-auth', nargs=2, type=str,
              help="Use basic authentication.", metavar='USER PASS')
@click.option('-d', '--digest-auth', nargs=2, type=str,
              help="Use digest authentication.", metavar='USER PASS')
@click.option(
    "--server/--no-server",
    default=True,
    help="Start a connection request server (on by default)."
)
@click.version_option(tr069.__version__)
def cli(acs_url, basic_auth, digest_auth, server):
    click.secho(
        f"Interactive TR-069 Client Session (version: {tr069.__version__})",
        fg="green", bold=True
    )

    init_cmds = [
        "import tr069"
    ]
    if server:
        init_cmds.append("serv = tr069.ConnectionRequestServer()")
    if basic_auth:
        auth = f', basic_auth=("{basic_auth[0]}", "{basic_auth[1]}")'
    elif digest_auth:
        auth = f', digest_auth=("{digest_auth[0]}", "{digest_auth[1]}")'
    else:
        auth = ""
    init_cmds.append(f'c = tr069.Client("{acs_url}"{auth})')
    init_cmds.append('c')

    console = TR069Console(init_cmds)
    console.interact("")


if __name__ == "__main__":  # pragma: no cover
    cli()
