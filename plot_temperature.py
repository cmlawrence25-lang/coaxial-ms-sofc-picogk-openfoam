import numpy as np
import matplotlib.pyplot as plt


def plotTemperatureProfile():
    z = np.linspace(-90, 90, 100)
    temp = 620 + 40 * np.exp(-((z / 70) ** 2))

    plt.figure(figsize=(8, 4))
    plt.plot(z, temp, color="#d62728", linewidth=2)
    plt.title("MS-SOFC Axial Temperature Profile")
    plt.xlabel("Axial position (mm)")
    plt.ylabel("Temperature (°C)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("temperature_plot.png", dpi=300)
    if plt.get_backend().lower() != "agg":
        plt.show()
    plt.close()


if __name__ == "__main__":
    plotTemperatureProfile()