N <- 100
S <- 10

# y is a positive integer 
alternateZoom <- function(x,y) {
  return (1+ (x^(-y)) / (-y));
}

exponents <- -10+0.01*runif(N)
vals <- 1-exp(exponents)
vals <- c(runif(S)*0.001, vals)

hist(log(1-vals))
hist(alternateZoom(10^-20 + 1-vals, 18))
