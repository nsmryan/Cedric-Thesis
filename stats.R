options(contrasts=c("contr.sum","contr.poly"))

require(nlme)
require(multcomp)
require(ez)

print('Starting stats')
writeLines("\n\n")

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
ezPrecis(percentStill_a)
writeLines("\n")

print('\nPercent Standing Still (b)')
summary(percentStillModel_b)
summary(glht(percentStillLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_b)
ezPrecis(percentStill_b)
writeLines("\n")

print('\nPercent Standing Still (c)')
summary(percentStillModel_c)
summary(glht(percentStillLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_c)
ezPrecis(percentStill_c)
writeLines("\n")

dev.off()


print('__________________________________________')
writeLines("\n\n")

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
ezPrecis(avgSpeed_a)
writeLines("\n")

print('\nAverage Speed (b)')
summary(avgSpeedModel_b)
plot(AverageSpeed ~ treatment, avgSpeed_b)
ezPrecis(avgSpeed_b)
writeLines("\n")

print('\nAverage Speed (c)')
summary(avgSpeedModel_c)
plot(AverageSpeed ~ treatment, avgSpeed_c)
ezPrecis(avgSpeed_c)
writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Starting Percent Middle')
location_a = read.csv("output/Location_60/Location_a")
location_b = read.csv("output/Location_60/Location_b")
location_c = read.csv("output/Location_60/Location_c")

locationModel_a = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_a)
locationModel_b = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_b)
locationModel_c = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

writeLines("\n")
print('location (a)')
summary(locationModel_a)
plot(Location ~ treatment, location_a)
ezPrecis(location_a)
writeLines("\n")

writeLines("\n")
print('Location (b)')
summary(locationModel_b)
plot(Location ~ treatment, location_b)
ezPrecis(location_b)
writeLines("\n")

writeLines("\n")
print('Location (c)')
summary(locationModel_c)
plot(Location ~ treatment, location_c)
ezPrecis(location_c)
writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Percent Middle (Full session)')
locationFull_a = read.csv("output/LocationFull/LocationFull_full_a")
locationFull_b = read.csv("output/LocationFull/LocationFull_full_b")
locationFull_c = read.csv("output/LocationFull/LocationFull_full_c")

locationFullModel_a = aov(LocationFull ~ treatment, locationFull_a)
locationFullModel_b = aov(LocationFull ~ treatment, locationFull_b)
locationFullModel_c = aov(LocationFull ~ treatment, locationFull_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('LocationFull (a)')
summary(locationFullModel_a)
plot(LocationFull ~ treatment, locationFull_a)
ezPrecis(locationFull_a)

writeLines("\n")

print('LocationFull (b)')
summary(locationFullModel_b)
plot(LocationFull ~ treatment, locationFull_b)
ezPrecis(locationFull_b)

writeLines("\n")

print('LocationFull (c)')
summary(locationFullModel_c)
plot(LocationFull ~ treatment, locationFull_c)
ezPrecis(locationFull_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed (Full session)')
averageSpeedFull_a = read.csv("output/AverageSpeedFull/AverageSpeedFull_full_a")
averageSpeedFull_b = read.csv("output/AverageSpeedFull/AverageSpeedFull_full_b")
averageSpeedFull_c = read.csv("output/AverageSpeedFull/AverageSpeedFull_full_c")

averageSpeedFullModel_a = aov(AverageSpeedFull ~ treatment, averageSpeedFull_a)
averageSpeedFullLME_a = lme(AverageSpeedFull ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedFull_a)

averageSpeedFullModel_b = aov(AverageSpeedFull ~ treatment, averageSpeedFull_b)
averageSpeedFullLME_b = lme(AverageSpeedFull ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedFull_b)

averageSpeedFullModel_c = aov(AverageSpeedFull ~ treatment, averageSpeedFull_c)
averageSpeedFullLME_c = lme(AverageSpeedFull ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedFull_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('AverageSpeedFull (a)')
summary(averageSpeedFullModel_a)
summary(glht(averageSpeedFullLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_a)
ezPrecis(averageSpeedFull_a)

writeLines("\n")

print('AverageSpeedFull (b)')
summary(averageSpeedFullModel_b)
summary(glht(averageSpeedFullLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_b)
ezPrecis(averageSpeedFull_b)

writeLines("\n")

print('AverageSpeedFull (c)')
summary(averageSpeedFullModel_c)
summary(glht(averageSpeedFullLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_c)
ezPrecis(averageSpeedFull_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed (Middle session)')
averageSpeedMid_a = read.csv("output/AverageSpeedMid/AverageSpeedMid_full_a")
averageSpeedMid_b = read.csv("output/AverageSpeedMid/AverageSpeedMid_full_b")
averageSpeedMid_c = read.csv("output/AverageSpeedMid/AverageSpeedMid_full_c")

averageSpeedMidModel_a = aov(AverageSpeedMid ~ treatment, averageSpeedMid_a)
averageSpeedMidLME_a = lme(AverageSpeedMid ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedMid_a)

averageSpeedMidModel_b = aov(AverageSpeedMid ~ treatment, averageSpeedMid_b)
averageSpeedMidLME_b = lme(AverageSpeedMid ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedMid_b)

averageSpeedMidModel_c = aov(AverageSpeedMid ~ treatment, averageSpeedMid_c)
averageSpeedMidLME_c = lme(AverageSpeedMid ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedMid_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('AverageSpeedMid (a)')
summary(averageSpeedMidModel_a)
summary(glht(averageSpeedMidLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedMid ~ treatment, averageSpeedMid_a)
ezPrecis(averageSpeedMid_a)

writeLines("\n")

print('AverageSpeedMid (b)')
summary(averageSpeedMidModel_b)
summary(glht(averageSpeedMidLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedMid ~ treatment, averageSpeedMid_b)
ezPrecis(averageSpeedMid_b)

writeLines("\n")

print('AverageSpeedMid (c)')
summary(averageSpeedMidModel_c)
summary(glht(averageSpeedMidLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedMid ~ treatment, averageSpeedMid_c)
ezPrecis(averageSpeedMid_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed (Edge session)')
averageSpeedEdge_a = read.csv("output/AverageSpeedEdge/AverageSpeedEdge_full_a")
averageSpeedEdge_b = read.csv("output/AverageSpeedEdge/AverageSpeedEdge_full_b")
averageSpeedEdge_c = read.csv("output/AverageSpeedEdge/AverageSpeedEdge_full_c")

averageSpeedEdgeModel_a = aov(AverageSpeedEdge ~ treatment, averageSpeedEdge_a)
averageSpeedEdgeLME_a = lme(AverageSpeedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedEdge_a)

averageSpeedEdgeModel_b = aov(AverageSpeedEdge ~ treatment, averageSpeedEdge_b)
averageSpeedEdgeLME_b = lme(AverageSpeedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedEdge_b)

averageSpeedEdgeModel_c = aov(AverageSpeedEdge ~ treatment, averageSpeedEdge_c)
averageSpeedEdgeLME_c = lme(AverageSpeedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedEdge_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('AverageSpeedEdge (a)')
summary(averageSpeedEdgeModel_a)
summary(glht(averageSpeedEdgeLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedEdge ~ treatment, averageSpeedEdge_a)
ezPrecis(averageSpeedEdge_a)

writeLines("\n")

print('AverageSpeedEdge (b)')
summary(averageSpeedEdgeModel_b)
summary(glht(averageSpeedEdgeLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedEdge ~ treatment, averageSpeedEdge_b)
ezPrecis(averageSpeedEdge_b)

writeLines("\n")

print('AverageSpeedEdge (c)')
summary(averageSpeedEdgeModel_c)
summary(glht(averageSpeedEdgeLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedEdge ~ treatment, averageSpeedEdge_c)
ezPrecis(averageSpeedEdge_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed (Corner session)')
averageSpeedCorner_a = read.csv("output/AverageSpeedCorner/AverageSpeedCorner_full_a")
averageSpeedCorner_b = read.csv("output/AverageSpeedCorner/AverageSpeedCorner_full_b")
averageSpeedCorner_c = read.csv("output/AverageSpeedCorner/AverageSpeedCorner_full_c")

averageSpeedCornerModel_a = aov(AverageSpeedCorner ~ treatment, averageSpeedCorner_a)
averageSpeedCornerLME_a = lme(AverageSpeedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedCorner_a)

averageSpeedCornerModel_b = aov(AverageSpeedCorner ~ treatment, averageSpeedCorner_b)
averageSpeedCornerLME_b = lme(AverageSpeedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedCorner_b)

averageSpeedCornerModel_c = aov(AverageSpeedCorner ~ treatment, averageSpeedCorner_c)
averageSpeedCornerLME_c = lme(AverageSpeedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageSpeedCorner_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('AverageSpeedCorner (a)')
summary(averageSpeedCornerModel_a)
summary(glht(averageSpeedCornerLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedCorner ~ treatment, averageSpeedCorner_a)
ezPrecis(averageSpeedCorner_a)

writeLines("\n")

print('AverageSpeedCorner (b)')
summary(averageSpeedCornerModel_b)
summary(glht(averageSpeedCornerLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedCorner ~ treatment, averageSpeedCorner_b)
ezPrecis(averageSpeedCorner_b)

writeLines("\n")

print('AverageSpeedCorner (c)')
summary(averageSpeedCornerModel_c)
summary(glht(averageSpeedCornerLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedCorner ~ treatment, averageSpeedCorner_c)
ezPrecis(averageSpeedCorner_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")
