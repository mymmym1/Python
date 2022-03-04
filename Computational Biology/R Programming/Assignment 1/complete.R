complete <- function(directory, id = 1:332){
  f = list.files(path = directory, pattern = "*.csv", full.names = TRUE)
  vector = c()  # create an empty vector
  for (i in id){
    initial = read.csv(f[i])
    good = complete.cases(initial[,2:3])
    final = initial[good,]
    numOfrows = nrow(final)
    vector = append(vector, numOfrows)
  }
  x = data.frame(id = id, nobs = vector)
  x
}
  
