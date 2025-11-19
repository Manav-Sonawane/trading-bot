import os
import click
from dotenv import load_dotenv

from bot import BasicBot
from logging_config import configure_logging

load_dotenv()
logger = configure_logging()

def get_bot():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_TESTNET_BASE")

    if not api_key or not api_secret:
        raise click.UsageError("API keys not found. Set them in .env first")
    
    return BasicBot(api_key, api_secret, base_url=base_url, testnet=True)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option("--quantity", required=True, type=float)
@click.option("--type", "ord_type", required=True, type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False))
@click.option("--price", type=float, default=None)
@click.option("--tif", "time_in_force", type=click.Choice(["GTC", "IOC", "FOK"], case_sensitive=False), default="GTC")

def place(symbol, side, quantity, ord_type, price, time_in_force):
    bot = get_bot()
    try:
        result = bot.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            ord_type=ord_type,
            price=price,
            time_in_force=time_in_force
        )
        click.echo(f"Order placed: {result}")
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        click.echo(f"Error placing order: {e}")

@cli.command()
@click.option("--symbol", required=True)
@click.option("--order_id", required=True, type=int)

def status(symbol, order_id):
    bot = get_bot()
    try:
        result = bot.get_order(symbol=symbol, order_id=order_id)
        click.echo(f"Order status: {result}")
    except Exception as e:
        logger.error(f"Error fetching order status: {e}")
        click.echo(f"Error fetching order status: {e}")

@cli.command()
@click.option("--symbol", required=True)
@click.option("--order_id", required=True, type=int)
def cancel(symbol, order_id):
    """Cancel an order"""
    bot = get_bot()
    try:
        result = bot.cancel_order(symbol, order_id)
        click.echo(result)
    except Exception as e:
        logger.exception("Cancel failed")
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()