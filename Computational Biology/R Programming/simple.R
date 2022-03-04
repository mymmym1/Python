add2 <- function(x, y){
  x + y
}

above10 <- function(x){
  use <- x > 10 #return a logical vector(T,F)
  x[use] #return subset of vector x that is >10
}

above <- function(x, n = 10){ #default=10
  use <- x > n 
  x[use] 
}

columnmean <- function(m, removeNA = TRUE){
  nc <- ncol(m) #how many columns in matrix m
  means <- numeric(nc) #initialize an empyty vector to all zeros 
  for(i in 1:nc){
    means[i] <- mean(m[,i])
  }
  means
}
