"""Entry points for Hypergraphical."""
import click
import logging

from .transcribe import transcribe


@click.group(invoke_without_command=True)
@click.version_option(
    prog_name='Hypergraphical', message='%(prog)s %(version)s')
@click.pass_context
def cli(ctx) -> None:
    """CLI for Hypergraphical."""
    configure_logging()

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(1)


cli.add_command(transcribe)


def configure_logging() -> None:
    """Configure logging to write to logs.txt."""
    log_format = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    root_logger = logging.getLogger()
    try:
        log_handler = logging.FileHandler('logs.txt', mode='w')
        root_logger.addHandler(log_handler)
    except Exception as e:
        print('Error configuring logs: {}'.format(e.message))


if __name__ == '__main__':
    cli()
