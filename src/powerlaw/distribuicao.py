import numpy as np
import matplotlib.pyplot as plt
import powerlaw as plw


def validaDistribuicao(graus, gamma):
    graus = [g for g in graus if g >= 1]
    fit = plw.Fit(graus, xmin=2, discrete=True)
    alpha = fit.power_law.alpha
    ks_stat = fit.power_law.KS()

    print("Ajuste Power Law:")
    print("  α (alpha):", alpha)
    print("  KS Statistic:", ks_stat)

    valores, contagens = np.unique(graus, return_counts=True)
    valores = valores[valores >= 1]
    contagens = contagens[: len(valores)]

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    axs[0].bar(valores, contagens, width=0.8, color="skyblue", edgecolor="black", label="Frequência Empírica")
    x = np.array(valores)
    y = x ** (-gamma)
    y *= max(contagens) / max(y)
    axs[0].plot(x, y, "r--", linewidth=2, label=f"k^-{gamma:.2f} (Power Law)")
    axs[0].set_xscale("log")
    axs[0].set_yscale("log")
    axs[0].set_xlim(left=1)
    axs[0].set_ylim(bottom=1)
    axs[0].set_title("Escala Log-Log")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].bar(valores, contagens, width=0.8, color="skyblue", edgecolor="black", label="Frequência Empírica")
    x_lin = np.linspace(min(valores), max(valores), 200)
    y_lin = x_lin ** (-gamma)
    y_lin *= max(contagens) / max(y_lin)
    axs[1].plot(x_lin, y_lin, "r--", linewidth=2, label=f"k^-{gamma:.2f} (Power Law)")
    axs[1].set_title("Escala Linear")
    axs[1].legend()
    axs[1].grid(True)

    plt.suptitle("Distribuição de Graus: Power Law Empírica vs Teórica", fontsize=15)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
