options(contrasts=c("contr.sum","contr.poly"))

require(nlme)
require(multcomp)

print('Starting stats')

print('Starting Percent Still')
percentStill_a = read.csv("output/PercentStill_60/PercentStill_a")
percentStill_b = read.csv("output/PercentStill_60/PercentStill_b")
percentStill_c = read.csv("output/PercentStill_60/PercentStill_c")

percentStillModel_a = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_a)
percentStillLME_a   = lme(PercentStill ~ treatment + time + treatment * time, random = ~ 1 | crayfishid / time, data=percentStill_a)

percentStillModel_b = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_b)
percentStillLME_b   = lme(PercentStill ~ treatment + time + treatment * time, random = ~ 1 | crayfishid / time, data=percentStill_b)

percentStillModel_c = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_c)
percentStillLME_c   = lme(PercentStill ~ treatment + time + treatment * time, random = ~ 1 | crayfishid / time, data=percentStill_c)

png("percentStill_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('\n\nPercent Standing Still (a)')
summary(percentStillModel_a)
summary(glht(percentStillLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_a)

print('\nPercent Standing Still (b)')
summary(percentStillModel_b)
summary(glht(percentStillLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_b)

print('\nPercent Standing Still (c)')
summary(percentStillModel_c)
summary(glht(percentStillLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_c)

dev.off()


print('\n__________________________________________\n')

print('Starting Average Still')
avgSpeed_a = read.csv("output/AverageSpeed_60/AverageSpeed_a")
avgSpeed_b = read.csv("output/AverageSpeed_60/AverageSpeed_b")
avgSpeed_c = read.csv("output/AverageSpeed_60/AverageSpeed_c")

avgSpeedModel_a = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_a)
avgSpeedModel_b = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_b)
avgSpeedModel_c = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_c)


png("averageSpeed_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('\n\nAverage Speed (a)')
summary(avgSpeedModel_a)
plot(AverageSpeed ~ treatment, avgSpeed_a)

print('\nAverage Speed (b)')
summary(avgSpeedModel_b)
plot(AverageSpeed ~ treatment, avgSpeed_b)

print('\nAverage Speed (c)')
summary(avgSpeedModel_c)
plot(AverageSpeed ~ treatment, avgSpeed_c)

dev.off()

print('\n__________________________________________\n')

