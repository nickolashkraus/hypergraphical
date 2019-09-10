import click

from .podcast import Podcast


@click.command()
@click.argument('key', required=True)
@click.argument('index', required=True)
def transcribe(*args, **kwargs) -> None:
    """
    Transcribe a podcast episode using AWS Transcribe.

    Use podcasts.yaml to determine podcast metadata.

    :param kwargs: dict of keyword arguments
    :type kwargs: dict
        * key: key of podcast from podcasts.yaml
        * index: episode index of podcast from podcasts.yaml
    """
    podcast = Podcast(*args, **kwargs)
    click.echo(str(podcast))
