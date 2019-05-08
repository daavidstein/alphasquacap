
# Discontinuity Regression with signal:
set.seed(223)
x <- seq(1,20,.25)
y_before <- rnorm(37, -1.5, 1.5) +x[1:37]*(1/2)
y_after <- rnorm(40, -3, 3) + (x[38:77])*4 - 30

example_df <- data.frame(x,c(y_before, y_after))
names(example_df)[2] <- "y"

# Plot of signal:
ggplot(example_df,aes(x=x,y=y))+
  geom_point() +
  geom_point(data=subset(example_df, x <= 10), aes(color = "1")) +
  geom_smooth(data=subset(example_df, x <= 10), aes(color = "1"), method='lm',formula=y~x,se=T) +
  geom_point(data=subset(example_df, x > 10), aes(color = "2")) +
  geom_smooth(data=subset(example_df, x > 10), aes(color  = "2"), method='lm',formula=y~x,se=T) +
  geom_vline(xintercept = 10, linetype='dashed') +
  ggtitle(label = "Example of Discontinuity Regression") +
  scale_color_manual(values = c("1" = "blue","2" = "red"),
                     labels = c("Before", "After")) +
  labs(x = "Time", y = "Response", color = "Treatment Period") +
  theme_minimal()


# Discontinuity Regression with NO signal:
set.seed(223)
x <- seq(1,20,.25)
y_before <- rnorm(37, -.5, .5) +x[1:37]*(1/3)
y_after <- rnorm(40, -.5, .5) + x[38:77]*(1/3)

example_df <- data.frame(x,c(y_before, y_after))
names(example_df)[2] <- "y"

# Plot of NO signal:
ggplot(example_df,aes(x=x,y=y))+
  geom_point() +
  geom_point(data=subset(example_df, x <= 10), aes(color = "1")) +
  geom_smooth(data=subset(example_df, x <= 10), aes(color = "1"), method='lm',formula=y~x,se=T) +
  geom_point(data=subset(example_df, x > 10), aes(color = "2")) +
  geom_smooth(data=subset(example_df, x > 10), aes(color  = "2"), method='lm',formula=y~x,se=T) +
  geom_vline(xintercept = 10, linetype='dashed') +
  ggtitle(label = "Example of Discontinuity Regression") +
  scale_color_manual(values = c("1" = "blue","2" = "red"),
                     labels = c("Before", "After")) +
  labs(x = "Time", y = "Response", color = "Treatment Period") +
  theme_minimal()