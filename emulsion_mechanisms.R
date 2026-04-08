library(ggplot2)
library(gridExtra)
library(grid)

# Set seed for reproducibility
set.seed(42)

# Function to create droplet positions
create_stable <- function() {
  # Randomly distributed droplets
  n <- 40
  data.frame(
    x = runif(n, 0, 10),
    y = runif(n, 0, 10),
    size = rnorm(n, 2, 0.3),
    type = "Estable"
  )
}

create_flocculation <- function() {
  # Clustered droplets
  n <- 40
  clusters <- rep(1:4, each = 10)
  x_centers <- c(2, 8, 2, 8)
  y_centers <- c(8, 8, 2, 2)
  
  data.frame(
    x = x_centers[clusters] + rnorm(n, 0, 0.8),
    y = y_centers[clusters] + rnorm(n, 0, 0.8),
    size = rnorm(n, 1.8, 0.2),
    type = "Floculación"
  )
}

create_creaming <- function() {
  # Droplets concentrated at top
  n <- 40
  data.frame(
    x = runif(n, 0, 10),
    y = runif(n, 6, 10),  # Concentrated at top
    size = rnorm(n, 2, 0.3),
    type = "Cremado"
  )
}

create_sedimentation <- function() {
  # Droplets concentrated at bottom
  n <- 40
  data.frame(
    x = runif(n, 0, 10),
    y = runif(n, 0, 4),  # Concentrated at bottom
    size = rnorm(n, 2, 0.3),
    type = "Sedimentación"
  )
}

create_coalescence <- function() {
  # Few large droplets with directional arrows
  data.frame(
    x = c(3, 7, 5),
    y = c(7, 7, 3),
    size = c(3.5, 3.5, 4.5),
    type = "Coalescencia"
  )
}

create_ostwald <- function() {
  # One central large droplet with smaller ones around (ripening)
  data.frame(
    x = c(5, 3, 2, 4, 6, 8, 7),
    y = c(5, 7, 4, 2, 7, 4, 6),
    size = c(5, 1.2, 0.8, 1.0, 1.3, 0.9, 1.1),
    type = "Maduración de Ostwald"
  )
}

# Combine all data
plot_data <- rbind(
  create_stable(),
  create_flocculation(),
  create_creaming(),
  create_sedimentation(),
  create_coalescence(),
  create_ostwald()
)

# Create labels for Spanish mechanisms
plot_data$type <- factor(plot_data$type, 
                          levels = c("Estable", "Floculación", "Cremado", 
                                    "Sedimentación", "Coalescencia", "Maduración de Ostwald"))

# Ensure coordinates are within bounds
plot_data$x <- pmin(pmax(plot_data$x, 0.5), 9.5)
plot_data$y <- pmin(pmax(plot_data$y, 0.5), 9.5)

# Create the main plot
p <- ggplot(plot_data, aes(x = x, y = y, size = size, fill = type)) +
  geom_point(shape = 21, color = "darkgoldenrod", alpha = 0.85) +
  facet_wrap(~ type, nrow = 2, ncol = 3) +
  scale_size(range = c(2, 8), guide = "none") +
  scale_fill_manual(values = rep("gold", 6), guide = "none") +
  theme_minimal() +
  theme(
    panel.background = element_rect(fill = "lightblue", color = "black", size = 0.8),
    panel.grid = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank(),
    axis.ticks = element_blank(),
    strip.text = element_text(size = 11, face = "bold", color = "black"),
    plot.title = element_text(size = 14, face = "bold", hjust = 0.5)
  ) +
  coord_fixed(xlim = c(0, 10), ylim = c(0, 10)) +
  labs(title = "Principales mecanismos de inestabilidad en emulsiones O/W")

print(p)

# Save high-quality version
ggsave("emulsion_mechanisms.png", p, width = 14, height = 8, dpi = 300, bg = "white")
print("Figura guardada como: emulsion_mechanisms.png")
