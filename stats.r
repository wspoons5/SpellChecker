setwd("c:/Users/Michael/Projects/spellChecker")
dat = read.csv("testOutcomes.csv", header=T)
dat$norvigSuccess = as.factor(dat$norvigSuccess)
dat$chiSquareSuccess = as.factor(dat$chiSquareSuccess)
dat$gtestSuccess = as.factor(dat$gtestSuccess)
dat$multinomialSuccess = as.factor(dat$multinomialSuccess)
dat$logfreq = log(dat$freq)
dat2 = dat[(dat$freq!=0),]


par(mfrow=c(2,2))
cdplot(dat2$norvigSuccess~dat2$incorrectLength, main="Norvig Model", ylab="success", xlab="length")
cdplot(dat2$gtestSuccess~dat2$incorrectLength, main="G-Test Model", ylab="success", xlab="length")
cdplot(dat2$chiSquareSuccess~dat2$incorrectLength, main="Chi-Square Model", ylab="success", xlab="length")
cdplot(dat2$multinomialSuccess~dat2$incorrectLength, main="Multinomial Model", ylab="success", xlab="length")

norvigLogit = glm(norvigSuccess~incorrectLength+logfreq+candidateCount, data=dat2, family="binomial")
gtestLogit = glm(gtestSuccess~incorrectLength+logfreq+candidateCount, data=dat2, family="binomial")
chisquareLogit = glm(chiSquareSuccess~incorrectLength+logfreq+candidateCount, data=dat2, family="binomial")
multinomialLogit = glm(multinomialSuccess~incorrectLength+logfreq+candidateCount, data=dat2, family="binomial")

summary(norvigLogit)
summary(gtestLogit)
summary(chisquareLogit)
summary(multinomialLogit)

summary(dat2$norvigSuccess)
summary(dat2$chiSquareSuccess)
summary(dat2$gtestSuccess)
summary(dat2$multinomialSuccess)