calsolarmean <- function(){
  good = complete.cases(file[,1:2])
  final = file[good,]
  numOflines = nrow(final)
  newframe = data.frame()
  for(l in 1:numOflines){
    if(final[l,]$Ozone>31 && final[l,]$Temp>90){
      newframe = rbind(newframe, final[l,])
    }
  }
  solarmean = mean(newframe[["Solar.R"]])
  solarmean
}