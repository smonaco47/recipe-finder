from src.hello_world import hello_world
import click

@click.command()
@click.option('--name', prompt='Your name')
def main(name):
    hello_world(name)


if __name__ == '__main__':
    main()