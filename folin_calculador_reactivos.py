"""
CALCULADOR DE CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU
Calcula los volúmenes de reactivos necesarios para preparar 6 puntos de calibración
"""

class CalculadorFolinCiocalteu:
    """
    Calcula volúmenes y reactivos para curva de calibración Folin-Ciocalteu
    """
    
    def __init__(self):
        self.volumen_final = 5  # mL
        self.concentracion_ac_galico = None
        self.volumen_folin = None
        self.concentracion_na2co3 = None
        self.puntos_calibracion = []
    
    def obtener_datos_iniciales(self):
        """
        Obtiene los datos iniciales del usuario
        """
        print("\n" + "=" * 80)
        print("CALCULADOR DE CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU")
        print("=" * 80)
        
        print("\n📋 PARÁMETROS DE LA SOLUCIÓN MADRE DE ÁCIDO GÁLICO:")
        print("-" * 80)
        
        try:
            self.concentracion_ac_galico = float(
                input("Concentración de la solución madre de Ácido Gálico (mg/mL): ")
            )
            
            print("\n📋 PARÁMETROS DEL REACTIVO FOLIN-CIOCALTEU:")
            print("-" * 80)
            self.volumen_folin = float(
                input("Volumen de reactivo Folin-Ciocalteu a usar en cada punto (mL): ")
            )
            
            print("\n📋 PARÁMETROS DEL CARBONATO DE SODIO:")
            print("-" * 80)
            self.concentracion_na2co3 = float(
                input("Concentración de Na₂CO₃ (% w/V): ")
            )
            
            print("\n✓ Datos capturados correctamente")
            
        except ValueError:
            print("❌ Error: Ingresa valores numéricos válidos")
            return False
        
        return True
    
    def generar_concentraciones(self):
        """
        Genera 6 puntos de calibración equiespaciados
        """
        print("\n" + "=" * 80)
        print("GENERACIÓN DE PUNTOS DE CALIBRACIÓN")
        print("=" * 80)
        
        print("\n¿Cómo deseas generar los 6 puntos?")
        print("1. Automático (0 - concentración máxima)")
        print("2. Manual (ingresa cada concentración)")
        
        opcion = input("\nSelecciona opción (1 o 2): ").strip()
        
        if opcion == '1':
            try:
                conc_maxima = float(
                    input("\nIngresa la concentración máxima deseada (mg/mL): ")
                )
                
                # Generar 6 puntos equiespaciados (incluye 0)
                self.puntos_calibracion = [
                    i * (conc_maxima / 5) for i in range(6)
                ]
                
            except ValueError:
                print("❌ Error: Ingresa un valor numérico válido")
                return False
        
        elif opcion == '2':
            print("\nIngresa las 6 concentraciones de ácido gálico (mg/mL):")
            try:
                for i in range(6):
                    conc = float(input(f"Concentración punto {i+1} (mg/mL): "))
                    self.puntos_calibracion.append(conc)
            except ValueError:
                print("❌ Error: Ingresa valores numéricos válidos")
                return False
        
        else:
            print("❌ Opción no válida")
            return False
        
        return True
    
    def calcular_volumenes(self):
        """
        Calcula los volúmenes de cada reactivo para cada punto
        """
        print("\n" + "=" * 80)
        print("CÁLCULO DE VOLÚMENES Y REACTIVOS")
        print("=" * 80)
        
        resultados = []
        
        for i, concentracion in enumerate(self.puntos_calibracion, 1):
            # Calcular volumen de ácido gálico necesario
            volumen_ac_galico = (concentracion * self.volumen_final) / self.concentracion_ac_galico
            
            # Calcular masa de Na₂CO₃ necesaria (w/V%)
            masa_na2co3 = (self.concentracion_na2co3 / 100) * self.volumen_final
            
            # Volumen de etanol para completar a 5 mL
            # Se asume que el Folin y Na₂CO₃ ocupan volumen
            volumen_etanol = self.volumen_final - self.volumen_folin - volumen_ac_galico - (masa_na2co3 / 1.05)
            
            # Si el volumen es negativo, ajustar
            if volumen_etanol < 0:
                volumen_etanol = 0
            
            resultado = {
                'punto': i,
                'concentracion_ag': concentracion,
                'volumen_ag': volumen_ac_galico,
                'volumen_folin': self.volumen_folin,
                'masa_na2co3': masa_na2co3,
                'volumen_etanol': volumen_etanol
            }
            
            resultados.append(resultado)
        
        return resultados
    
    def mostrar_resultados_tabla(self, resultados):
        """
        Muestra los resultados en forma de tabla
        """
        print("\n" + "=" * 120)
        print("TABLA DE PREPARACIÓN DE PUNTOS DE CALIBRACIÓN")
        print("=" * 120)
        
        print(f"\n{'Punto':<8} {'[AG]':<15} {'Vol. AG':<15} {'Vol. Folin':<15} {'Masa Na₂CO₃':<15} {'Vol. Etanol':<15}")
        print(f"{'':8} {'(mg/mL)':<15} {'(mL)':<15} {'(mL)':<15} {'(g)':<15} {'(mL)':<15}")
        print("-" * 120)
        
        for resultado in resultados:
            print(f"{resultado['punto']:<8} "
                  f"{resultado['concentracion_ag']:<15.4f} "
                  f"{resultado['volumen_ag']:<15.4f} "
                  f"{resultado['volumen_folin']:<15.4f} "
                  f"{resultado['masa_na2co3']:<15.4f} "
                  f"{resultado['volumen_etanol']:<15.4f}")
        
        print("-" * 120)
        print(f"VOLUMEN FINAL: {self.volumen_final} mL para cada punto")
        print("=" * 120)
    
    def mostrar_resultados_detallados(self, resultados):
        """
        Muestra los resultados de forma detallada para cada punto
        """
        print("\n" + "=" * 80)
        print("PROCEDIMIENTO DETALLADO DE PREPARACIÓN")
        print("=" * 80)
        
        for resultado in resultados:
            print(f"\n{'─' * 80}")
            print(f"PUNTO {resultado['punto']} - Concentración: {resultado['concentracion_ag']:.4f} mg/mL")
            print(f"{'─' * 80}")
            
            print(f"\n  REACTIVOS NECESARIOS:")
            print(f"  ┌─ Ácido Gálico (solución madre {self.concentracion_ac_galico} mg/mL):")
            print(f"  │  └─ Volumen a tomar: {resultado['volumen_ag']:.4f} mL")
            
            print(f"\n  ├─ Reactivo Folin-Ciocalteu:")
            print(f"  │  └─ Volumen a agregar: {resultado['volumen_folin']:.4f} mL")
            
            print(f"\n  ├─ Carbonato de Sodio (Na₂CO₃):")
            print(f"  │  ├─ Concentración: {self.concentracion_na2co3}% w/V")
            print(f"  │  └─ Masa a pesar: {resultado['masa_na2co3']:.4f} g")
            
            print(f"\n  └─ Etanol (para completar volumen):")
            print(f"     └─ Volumen a agregar: {resultado['volumen_etanol']:.4f} mL")
            
            print(f"\n  PROCEDIMIENTO:")
            print(f"  1. En un matraz de 5 mL, agregar {resultado['volumen_ag']:.4f} mL de AG")
            print(f"  2. Agregar {resultado['volumen_folin']:.4f} mL de reactivo Folin-Ciocalteu")
            print(f"  3. Agregar {resultado['masa_na2co3']:.4f} g de Na₂CO₃")
            print(f"  4. Agregar {resultado['volumen_etanol']:.4f} mL de etanol")
            print(f"  5. Mezclar bien")
            print(f"  6. Dejar reposar 2-5 minutos a temperatura ambiente")
            print(f"  7. Medir absorbancia a 765 nm en UV-Vis")
        
        print(f"\n{'=' * 80}")
    
    def exportar_resultados(self, resultados):
        """
        Exporta los resultados a un archivo de texto
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"calibracion_folin_{timestamp}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("PARÁMETROS INICIALES:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Concentración Ácido Gálico (solución madre): {self.concentracion_ac_galico} mg/mL\n")
            f.write(f"Volumen Reactivo Folin-Ciocalteu por punto: {self.volumen_folin} mL\n")
            f.write(f"Concentración Na₂CO₃: {self.concentracion_na2co3}% w/V\n")
            f.write(f"Volumen final de cada solución: {self.volumen_final} mL\n\n")
            
            f.write("TABLA RESUMEN:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Punto':<8} {'[AG]':<15} {'Vol. AG':<15} {'Vol. Folin':<15} {'Masa Na₂CO₃':<15}\n")
            f.write(f"{'':8} {'(mg/mL)':<15} {'(mL)':<15} {'(mL)':<15} {'(g)':<15}\n")
            f.write("-" * 80 + "\n")
            
            for resultado in resultados:
                f.write(f"{resultado['punto']:<8} "
                       f"{resultado['concentracion_ag']:<15.4f} "
                       f"{resultado['volumen_ag']:<15.4f} "
                       f"{resultado['volumen_folin']:<15.4f} "
                       f"{resultado['masa_na2co3']:<15.4f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("PROCEDIMIENTO DETALLADO:\n")
            f.write("=" * 80 + "\n\n")
            
            for resultado in resultados:
                f.write(f"PUNTO {resultado['punto']} - [{resultado['concentracion_ag']:.4f} mg/mL]\n")
                f.write("-" * 80 + "\n")
                f.write(f"• Ácido Gálico: {resultado['volumen_ag']:.4f} mL\n")
                f.write(f"• Folin-Ciocalteu: {resultado['volumen_folin']:.4f} mL\n")
                f.write(f"• Carbonato de Sodio: {resultado['masa_na2co3']:.4f} g ({self.concentracion_na2co3}% w/V)\n")
                f.write(f"• Etanol: {resultado['volumen_etanol']:.4f} mL\n")
                f.write(f"• VOLUMEN TOTAL: {self.volumen_final} mL\n\n")
        
        print(f"\n✓ Resultados exportados a: {nombre_archivo}")
        return nombre_archivo
    
    def ejecutar(self):
        """
        Ejecuta el programa completo
        """
        if not self.obtener_datos_iniciales():
            return
        
        if not self.generar_concentraciones():
            return
        
        resultados = self.calcular_volumenes()
        
        # Mostrar resultados
        self.mostrar_resultados_tabla(resultados)
        self.mostrar_resultados_detallados(resultados)
        
        # Preguntar si exportar
        exportar = input("\n¿Deseas exportar los resultados a un archivo? (s/n): ").strip().lower()
        if exportar == 's':
            self.exportar_resultados(resultados)
        
        print("\n✓ Proceso completado")


def main():
    """
    Función principal
    """
    calculador = CalculadorFolinCiocalteu()
    
    while True:
        calculador.ejecutar()
        
        continuar = input("\n¿Deseas generar otra curva de calibración? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
