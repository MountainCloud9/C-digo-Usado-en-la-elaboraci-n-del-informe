library(dplyr)
library(tidyr)
library(ggplot2)
library(ggpubr)

# 1) Tus datos (actualiza conc con valores reales del gráfico: ~0-100 µg/mL)
df_wide <- data.frame(
  conc = c(0, 20, 40, 60, 80, 100),  # Ajusta según tu eje X
  ABS1 = c(0.032, 0.039, 0.071, 0.122, 0.150, 0.194),
  ABS2 = c(0.027, 0.064, 0.161, 0.189, 0.264, 0.318),
  ABS3 = c(0.028, 0.044, 0.082, 0.131, 0.196, 0.226),
  Promedio = c(0.029, 0.049, 0.10466667, 0.14733333, 0.20333333, 0.246)
)

# 2) Formato largo para corridas
df_long <- df_wide %>%
  pivot_longer(cols = starts_with("ABS"), names_to = "run", values_to = "abs")

# 3) Solo promedios para la recta
df_mean <- df_wide %>% select(conc, Promedio) %>% rename(abs_mean = Promedio)

# 4) Gráfico monocromático
p <- ggplot(df_long, aes(x = conc, y = abs)) +
  
  # Puntos de las 3 corridas en escala de grises
  geom_point(aes(color = run, shape = run), size = 2.5, alpha = 0.7) +
  
  # Puntos de promedios (negros, más grandes)
  geom_point(data = df_mean, aes(x = conc, y = abs_mean),
             color = "black", size = 4, shape = 16) +
  
  # Línea de regresión SOLO en promedios (negra gruesa)
  geom_smooth(data = df_mean, aes(x = conc, y = abs_mean),
              method = "lm", se = FALSE, color = "black", size = 1.2) +
  
  # Ecuación + R² para la recta de promedios
  stat_regline_equation(
    data = df_mean, aes(x = conc, y = abs_mean,
                        label = paste(..eq.label.., ..rr.label.., sep = "~`,~"),
                        parse = TRUE),
    inherit.aes = FALSE,
    label.x.npc = "left", label.y.npc = "top"
  ) +
  
  # Escala monocromática
  scale_color_grey(start = 0.3, end = 0.8, name = "Corrida") +
  scale_shape_manual(values = c("ABS1" = 16, "ABS2" = 17, "ABS3" = 15),
                     name = "Corrida") +
  
  labs(x = "Concentración de ácido gálico (µg/mL)",
       y = "Absorbancia (a.u.)",
       title = "Curva de calibración de ácido gálico (Folin-Ciocalteu)") +
  
  theme_bw(base_size = 12) +
  theme(legend.position = "top",
        panel.grid.minor = element_blank())

print(p)
