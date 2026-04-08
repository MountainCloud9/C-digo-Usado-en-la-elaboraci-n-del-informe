import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime

class FolinCiocalteuCalibration:
    """
    Clase para gestionar curvas de calibración con reactivo Folin-Ciocalteu
    """
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.calibration_params = None
        self.r_squared = None
        
    def prepare_solutions(self, concentration_ag_mg_ml, concentration_na2co3_wv, 
                         volume_final_ml=5):
        """
        Calcula los volúmenes necesarios para preparar soluciones
        
        Parameters:
        -----------
        concentration_ag_mg_ml : float
            Concentración de ácido gálico en mg/mL
        concentration_na2co3_wv : float
            Concentración de carbonato de sodio en % w/V
        volume_final_ml : float
            Volumen final de solución (default: 5 mL)
        
        Returns:
        --------
        dict : Información de preparación de la solución
        """
        
        print("=" * 70)
        print("PREPARACIÓN DE SOLUCIÓN FOLIN-CIOCALTEU")
        print("=" * 70)
        
        # Cálculos básicos
        mass_na2co3_needed = (concentration_na2co3_wv / 100) * volume_final_ml
        
        prep_info = {
            'concentracion_ag': concentration_ag_mg_ml,
            'concentracion_na2co3': concentration_na2co3_wv,
            'volumen_final': volume_final_ml,
            'masa_na2co3': mass_na2co3_needed,
            'volumen_etanol': volume_final_ml - (mass_na2co3_needed / 1.05)  # Densidad aproximada Na2CO3
        }
        
        print(f"\n✓ Ácido Gálico: {concentration_ag_mg_ml} mg/mL")
        print(f"✓ Carbonato de Sodio: {concentration_na2co3_wv}% w/V")
        print(f"✓ Volumen final de solución: {volume_final_ml} mL")
        print(f"\nCálculos:")
        print(f"  - Masa de Na₂CO₃ requerida: {mass_na2co3_needed:.4f} g")
        print(f"  - Volumen de etanol aprox.: {prep_info['volumen_etanol']:.2f} mL")
        
        return prep_info
    
    def input_calibration_data(self):
        """
        Ingresa datos de calibración interactivamente
        """
        print("\n" + "=" * 70)
        print("INGRESO DE DATOS DE CALIBRACIÓN")
        print("=" * 70)
        
        data_points = []
        
        print("\nIngresa los pares de datos (Concentración en mg/mL, Absorbancia a 765 nm)")
        print("Escribe 'fin' cuando termines.\n")
        
        i = 1
        while True:
            try:
                conc_input = input(f"Punto {i} - Concentración (mg/mL) [o 'fin']: ").strip()
                
                if conc_input.lower() == 'fin':
                    if len(data_points) < 3:
                        print("⚠ Necesitas al menos 3 puntos para una curva válida.")
                        continue
                    break
                
                concentration = float(conc_input)
                absorbance = float(input(f"Punto {i} - Absorbancia (765 nm): ").strip())
                
                data_points.append({
                    'Concentración (mg/mL)': concentration,
                    'Absorbancia (765 nm)': absorbance
                })
                
                print(f"✓ Punto {i} registrado\n")
                i += 1
                
            except ValueError:
                print("❌ Error: Ingresa números válidos.\n")
        
        self.data = pd.DataFrame(data_points)
        print("\n" + "=" * 70)
        print("DATOS INGRESADOS:")
        print(self.data.to_string(index=False))
        print("=" * 70)
    
    def linear_regression(self, x, y):
        """
        Realiza regresión lineal
        """
        def linear_function(x, a, b):
            return a * x + b
        
        try:
            params, _ = curve_fit(linear_function, x, y)
            
            # Calcular R²
            y_pred = linear_function(x, *params)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            self.calibration_params = params
            self.r_squared = r_squared
            
            return params, r_squared
            
        except Exception as e:
            print(f"❌ Error en regresión: {e}")
            return None, None
    
    def analyze_calibration(self):
        """
        Analiza la curva de calibración
        """
        if self.data.empty:
            print("❌ No hay datos cargados. Ingresa primero los datos de calibración.")
            return
        
        print("\n" + "=" * 70)
        print("ANÁLISIS DE CALIBRACIÓN")
        print("=" * 70)
        
        x = self.data['Concentración (mg/mL)'].values
        y = self.data['Absorbancia (765 nm)'].values
        
        # Regresión lineal
        params, r_squared = self.linear_regression(x, y)
        
        if params is None:
            return
        
        a, b = params
        
        print(f"\nEcuación de la recta:")
        print(f"  Absorbancia = {a:.6f} × Concentración + {b:.6f}")
        print(f"\nCoeficiente de determinación (R²): {r_squared:.6f}")
        print(f"Correlación (r): {np.sqrt(r_squared):.6f}")
        
        # Estadísticas
        print(f"\nEstadísticas:")
        print(f"  Concentración mínima: {x.min():.4f} mg/mL")
        print(f"  Concentración máxima: {x.max():.4f} mg/mL")
        print(f"  Absorbancia mínima: {y.min():.4f}")
        print(f"  Absorbancia máxima: {y.max():.4f}")
        print(f"  Pendiente (sensibilidad): {a:.6f}")
        print(f"  Intercepto: {b:.6f}")
        
        return a, b, r_squared
    
    def plot_calibration_curve(self, save_plot=False):
        """
        Visualiza la curva de calibración
        """
        if self.data.empty:
            print("❌ No hay datos para graficar.")
            return
        
        x = self.data['Concentración (mg/mL)'].values
        y = self.data['Absorbancia (765 nm)'].values
        
        # Crear puntos de la línea ajustada
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = self.calibration_params[0] * x_line + self.calibration_params[1]
        
        # Crear figura
        plt.figure(figsize=(10, 6))
        
        # Graficar puntos experimentales
        plt.scatter(x, y, color='red', s=100, label='Datos experimentales', zorder=3)
        
        # Graficar línea ajustada
        plt.plot(x_line, y_line, 'b-', linewidth=2, 
                label=f'Ajuste lineal (R² = {self.r_squared:.4f})')
        
        # Configurar ejes y etiquetas
        plt.xlabel('Concentración de Ácido Gálico (mg/mL)', fontsize=12, fontweight='bold')
        plt.ylabel('Absorbancia (λ = 765 nm)', fontsize=12, fontweight='bold')
        plt.title('Curva de Calibración Folin-Ciocalteu', fontsize=14, fontweight='bold')
        
        # Grid
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Leyenda
        a, b = self.calibration_params
        ecuacion_text = f'y = {a:.6f}x + {b:.6f}'
        plt.text(0.5, 0.95, ecuacion_text, transform=plt.gca().transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                verticalalignment='top', horizontalalignment='center', fontsize=10)
        
        plt.legend(fontsize=10, loc='lower right')
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"calibration_curve_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✓ Gráfico guardado como: {filename}")
        
        plt.show()
    
    def predict_concentration(self, absorbance):
        """
        Predice la concentración a partir de una absorbancia
        
        Parameters:
        -----------
        absorbance : float
            Valor de absorbancia medido
        
        Returns:
        --------
        float : Concentración predicha en mg/mL
        """
        if self.calibration_params is None:
            print("❌ No hay parámetros de calibración. Realiza primero el análisis.")
            return None
        
        a, b = self.calibration_params
        concentration = (absorbance - b) / a
        
        return concentration
    
    def export_results(self, filename=None):
        """
        Exporta los resultados a un archivo
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"calibration_results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RESULTADOS DE CALIBRACIÓN FOLIN-CIOCALTEU\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            # Datos
            f.write("DATOS DE CALIBRACIÓN:\n")
            f.write(self.data.to_string(index=False))
            f.write("\n\n")
            
            # Parámetros
            if self.calibration_params is not None:
                a, b = self.calibration_params
                f.write("PARÁMETROS DE CALIBRACIÓN:\n")
                f.write(f"  Ecuación: Absorbancia = {a:.6f} × Concentración + {b:.6f}\n")
                f.write(f"  R² = {self.r_squared:.6f}\n")
                f.write(f"  Correlación (r) = {np.sqrt(self.r_squared):.6f}\n")
        
        print(f"\n✓ Resultados exportados a: {filename}")


def main():
    """
    Función principal - Menú interactivo
    """
    calibration = FolinCiocalteuCalibration()
    
    while True:
        print("\n" + "=" * 70)
        print("ANALIZADOR DE CALIBRACIÓN FOLIN-CIOCALTEU")
        print("=" * 70)
        print("\n1. Calcular volúmenes para preparar solución")
        print("2. Ingresar datos de calibración")
        print("3. Analizar curva de calibración")
        print("4. Graficar curva de calibración")
        print("5. Predecir concentración desde absorbancia")
        print("6. Exportar resultados")
        print("7. Salir")
        
        option = input("\nSelecciona una opción (1-7): ").strip()
        
        if option == '1':
            try:
                ag = float(input("Ingresa concentración de Ácido Gálico (mg/mL): "))
                na2co3 = float(input("Ingresa concentración de Na₂CO₃ (% w/V): "))
                vol = float(input("Ingresa volumen final (mL) [default=5]: ") or "5")
                calibration.prepare_solutions(ag, na2co3, vol)
            except ValueError:
                print("❌ Error: Ingresa valores numéricos válidos.")
        
        elif option == '2':
            calibration.input_calibration_data()
        
        elif option == '3':
            calibration.analyze_calibration()
        
        elif option == '4':
            save = input("¿Guardar gráfico? (s/n): ").lower() == 's'
            calibration.plot_calibration_curve(save_plot=save)
        
        elif option == '5':
            if calibration.calibration_params is None:
                print("❌ Primero debes analizar la calibración.")
            else:
                try:
                    abs_value = float(input("Ingresa el valor de absorbancia: "))
                    conc = calibration.predict_concentration(abs_value)
                    print(f"\n✓ Concentración predicha: {conc:.4f} mg/mL")
                except ValueError:
                    print("❌ Ingresa un valor numérico válido.")
        
        elif option == '6':
            calibration.export_results()
        
        elif option == '7':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    main()
    