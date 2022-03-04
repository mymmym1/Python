maxOzone5 <- function(){
  newframe = data.frame()
  for(l in 1:153){
    if(file[l,]$Month == 5){
      newframe = rbind(newframe, file[l,])
    }
  }
  maxOz = max(newframe$Ozone, na.rm = T)
  maxOz
}
