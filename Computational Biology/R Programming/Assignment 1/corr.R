corr <- function(directory, threshold = 0) {
  f = list.files(path = directory, pattern = "*.csv", full.names = TRUE)
  correlations <- vector("numeric", length = 0)  # initialize an empty numeric vector
  for (i in 1:length(f)){
    initial = read.csv(f[i])
    good = complete.cases(initial[,2:3])
    final = initial[good,]
    numOfrows = nrow(final)
    # calculates the correlation between sulfate and nitrate where the number of
    # completely observed cases is greater than the threshold. 
    if (numOfrows > threshold) {
      correlations = c(correlations, cor(final$sulfate, final$nitrate))
    }
  }
  correlations
}