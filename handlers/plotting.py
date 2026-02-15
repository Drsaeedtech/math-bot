from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sympy import sympify, symbols, lambdify
from io import BytesIO

x, y = symbols('x y')

# ---------- رسم نمودار 2 بعدی ----------
async def plot_2d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("plot "):
        return

    expr_text = text[5:]
    try:
        expr = sympify(expr_text)
        # تبدیل sympy expression به تابع numpy
        f = lambdify(x, expr, modules=['numpy'])

        X = np.linspace(-10, 10, 400)
        Y = f(X)

        plt.figure()
        plt.plot(X, Y)
        plt.title(f"y = {expr_text}")
        plt.grid(True)

        bio = BytesIO()
        plt.savefig(bio, format='png')
        bio.seek(0)
        plt.close()

        await update.message.reply_photo(photo=bio)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا در رسم نمودار 2D: {e}")

# ---------- رسم نمودار 3 بعدی ----------
async def plot_3d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("plot3d "):
        return

    expr_text = text[7:]
    try:
        expr = sympify(expr_text)
        f = lambdify((x, y), expr, modules=['numpy'])

        X = np.linspace(-5, 5, 100)
        Y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = f(X, Y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')

        bio = BytesIO()
        plt.savefig(bio, format='png')
        bio.seek(0)
        plt.close()

        await update.message.reply_photo(photo=bio)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا در رسم نمودار 3D: {e}")
