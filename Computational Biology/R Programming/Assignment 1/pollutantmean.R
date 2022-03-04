pollutantmean <- function(directory, pollutant, id = 1:332) {
  f = list.files(path = directory, pattern = "*.csv", full.names = TRUE)
  d = data.frame()  # create an empty data frame
  for (i in id){
    initial = read.csv(f[i])
    d = rbind(d, initial)  # combine data frame by rows
  }
  m = mean(d[[pollutant]], na.rm = TRUE)
  m  
}
# Console: 
# > pollutantmean("E:/My Documents/study material/CS/computational biology/R Programming/Assignment 1/specdata", "sulfate", 331:332)