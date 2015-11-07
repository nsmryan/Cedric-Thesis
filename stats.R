options(contrasts=c("contr.sum","contr.poly"))

require(nlme)
require(multcomp)
require(ez)

# TODO finish abstracting function, make one for non-time varying data
#      express the rest of the program with these functions
#      look at ezANOVA again. try table(rows, cols) to get exp design
#processStat <- function(name, filePath, fileName, dv) {
#  print('Starting New Section')
#  writeLines("\n\n")
#
#  print(name)
#  dataset_a = read.csv(paste0(filePath, fileName, "_a"))
#  dataset_b = read.csv(paste0(filePath, fileName, "_b"))
#  dataset_c = read.csv(paste0(filePath, fileName, "_c"))
#
#  datasetModel_a = aov(dv ~ treatment*time + Error(crayfishid/time) + time, dataset_a)
#  datasetLME_a   = lme(dv ~ treatment + time, random = ~ 1 | crayfishid / time, data=dataset_a)
#
#  datasetModel_b = aov(dv ~ treatment*time + Error(crayfishid/time) + time, dataset_b)
#  datasetLME_b   = lme(dv ~ treatment + time, random = ~ 1 | crayfishid / time, data=dataset_b)
#
#  datasetModel_c = aov(dv ~ treatment*time + Error(crayfishid/time) + time, dataset_c)
#  datasetLME_c   = lme(dv ~ treatment + time, random = ~ 1 | crayfishid / time, data=dataset_c)
#
#  png(paste0(name, ".png"), width=1000, height=400)
#  par(mfrow=c(1, 3))
#
#  print(paste0(name, " (a)"))
#  summary(percentStillModel_a)
#  summary(glht(datasetModel_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
#  plot(PercentStill ~ treatment, datasetModel_a)
#  ezPrecis(datasetModel_a)
#  writeLines("\n")
#
#  print(paste0(name, " (b)"))
#  summary(percentStillModel_b)
#  summary(glht(datasetModel_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
#  plot(PercentStill ~ treatment, datasetModel_b)
#  ezPrecis(datasetModel_b)
#  writeLines("\n")
#
#  print(paste0(name, " (c)"))
#  summary(datasetModel_c)
#  summary(glht(datasetModel_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
#  plot(PercentStill ~ treatment, datasetModel_c)
#  ezPrecis(datasetModel_c)
#  writeLines("\n")
#
#  dev.off()
#}

print('Starting stats')
writeLines("\n\n")

print('Percent Time Standing Still 60 Second Increments')
percentStill_a = read.csv("output/PercentStill_60/PercentStill_a")
percentStill_b = read.csv("output/PercentStill_60/PercentStill_b")
percentStill_c = read.csv("output/PercentStill_60/PercentStill_c")

percentStillModel_a = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_a)
percentStillLME_a   = lme(PercentStill ~ treatment + time, random = ~ 1 | crayfishid / time, data=percentStill_a)

percentStillModel_b = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_b)
percentStillLME_b   = lme(PercentStill ~ treatment + time, random = ~ 1 | crayfishid / time, data=percentStill_b)

percentStillModel_c = aov(PercentStill ~ treatment*time + Error(crayfishid/time) + time, percentStill_c)
percentStillLME_c   = lme(PercentStill ~ treatment + time, random = ~ 1 | crayfishid / time, data=percentStill_c)

png("percentStill_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('\n\nPercent Time Standing Still 60 Second Increments (a)')
summary(percentStillModel_a)
summary(percentStillLME_a)
summary(glht(percentStillLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_a)
ezPrecis(percentStill_a)
writeLines("\n")

print('\nPercent Time Standing Still 60 Second Increments (b)')
summary(percentStillModel_b)
summary(percentStillLME_b)
summary(glht(percentStillLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_b)
ezPrecis(percentStill_b)
writeLines("\n")

print('\nPercent Time Standing Still 60 Second Increments (c)')
summary(percentStillModel_c)
summary(percentStillLME_b)
summary(glht(percentStillLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(PercentStill ~ treatment, percentStill_c)
ezPrecis(percentStill_c)
writeLines("\n")

dev.off()


print('__________________________________________')
writeLines("\n\n")

print('Average Speed')
avgSpeed_a = read.csv("output/AverageSpeed_60/AverageSpeed_a")
avgSpeed_b = read.csv("output/AverageSpeed_60/AverageSpeed_b")
avgSpeed_c = read.csv("output/AverageSpeed_60/AverageSpeed_c")

avgSpeedModel_a = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_a)
avgSpeedModel_b = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_b)
avgSpeedModel_c = aov(AverageSpeed ~ treatment*time + Error(crayfishid/time) + time, avgSpeed_c)


png("averageSpeed_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Average Speed 60 Second Increments (a)')
summary(avgSpeedModel_a)
plot(AverageSpeed ~ treatment, avgSpeed_a)
ezPrecis(avgSpeed_a)
writeLines("\n")

print('Average Speed 60 Second Increments (b)')
summary(avgSpeedModel_b)
plot(AverageSpeed ~ treatment, avgSpeed_b)
ezPrecis(avgSpeed_b)
writeLines("\n")

print('Average Speed 60 Second Increments (c)')
summary(avgSpeedModel_c)
plot(AverageSpeed ~ treatment, avgSpeed_c)
ezPrecis(avgSpeed_c)
writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Percent Time Spent in Middle (per minute)')
location_a = read.csv("output/Location_60/Location_a")
location_b = read.csv("output/Location_60/Location_b")
location_c = read.csv("output/Location_60/Location_c")

locationModel_a = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_a)
locationModel_b = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_b)
locationModel_c = aov(Location ~ treatment*time + Error(crayfishid/time) + time, location_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

writeLines("\n")
print('Location 60 Second Increments (a)')
summary(locationModel_a)
plot(Location ~ treatment, location_a)
ezPrecis(location_a)
writeLines("\n")

writeLines("\n")
print('Location 60 Second Increments (b)')
summary(locationModel_b)
plot(Location ~ treatment, location_b)
ezPrecis(location_b)
writeLines("\n")

writeLines("\n")
print('Location 60 Second Increments (c)')
summary(locationModel_c)
plot(Location ~ treatment, location_c)
ezPrecis(location_c)
writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Percent Time Spent in Middle (Full session)')
locationFull_a = read.csv("output/LocationFull/LocationFull_full_a")
locationFull_b = read.csv("output/LocationFull/LocationFull_full_b")
locationFull_c = read.csv("output/LocationFull/LocationFull_full_c")

locationFullModel_a = aov(LocationFull ~ treatment, locationFull_a)
locationFullModel_b = aov(LocationFull ~ treatment, locationFull_b)
locationFullModel_c = aov(LocationFull ~ treatment, locationFull_c)


png("location_60.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Time Spend in Middle (a)')
summary(locationFullModel_a)
plot(LocationFull ~ treatment, locationFull_a)
ezPrecis(locationFull_a)

writeLines("\n")

print('Percent Time Spent in Middle (b)')
summary(locationFullModel_b)
plot(LocationFull ~ treatment, locationFull_b)
ezPrecis(locationFull_b)

writeLines("\n")

print('Percent Time Spent in Middle (c)')
summary(locationFullModel_c)
plot(LocationFull ~ treatment, locationFull_c)
ezPrecis(locationFull_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed (Over All session)')
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

print('Average Speed Over All (a)')
summary(averageSpeedFullModel_a)
summary(glht(averageSpeedFullLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_a)
ezPrecis(averageSpeedFull_a)

writeLines("\n")

print('Average Speed Over All (b)')
summary(averageSpeedFullModel_b)
summary(glht(averageSpeedFullLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_b)
ezPrecis(averageSpeedFull_b)

writeLines("\n")

print('Average SSpeed Over All (c)')
summary(averageSpeedFullModel_c)
summary(glht(averageSpeedFullLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AverageSpeedFull ~ treatment, averageSpeedFull_c)
ezPrecis(averageSpeedFull_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")


print('Average Speed while in Middle')
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


print('Average Speed While on Edge')
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


print('Average Speed While in Corner)')
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

print('Average Time Paused (Full session)')
averageTimePausedFull_a = read.csv("output/AvgTimePausedFull/AvgTimePausedFull_full_a")
averageTimePausedFull_b = read.csv("output/AvgTimePausedFull/AvgTimePausedFull_full_b")
averageTimePausedFull_c = read.csv("output/AvgTimePausedFull/AvgTimePausedFull_full_c")

averageTimePausedFullModel_a = aov(AvgTimePausedFull ~ treatment, averageTimePausedFull_a)
averageTimePausedFullLME_a = lme(AvgTimePausedFull ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedFull_a)

averageTimePausedFullModel_b = aov(AvgTimePausedFull ~ treatment, averageTimePausedFull_b)
averageTimePausedFullLME_b = lme(AvgTimePausedFull ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedFull_b)

averageTimePausedFullModel_c = aov(AvgTimePausedFull ~ treatment, averageTimePausedFull_c)
averageTimePausedFullLME_c = lme(AvgTimePausedFull ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedFull_c)


png("averageTimePaused.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Average Time Paused (a)')
summary(averageTimePausedFullModel_a)
summary(glht(averageTimePausedFullLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedFull ~ treatment, averageTimePausedFull_a)
ezPrecis(averageTimePausedFull_a)

writeLines("\n")

print('Average Time Paused (b)')
summary(averageTimePausedFullModel_b)
summary(glht(averageTimePausedFullLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedFull ~ treatment, averageTimePausedFull_b)
ezPrecis(averageTimePausedFull_b)

writeLines("\n")

print('Average Time Paused (c)')
summary(averageTimePausedFullModel_c)
summary(glht(averageTimePausedFullLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedFull ~ treatment, averageTimePausedFull_c)
ezPrecis(averageTimePausedFull_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Average Time Paused Middle (Full session)')
averageTimePausedMiddle_a = read.csv("output/AvgTimePausedMiddle/AvgTimePausedMiddle_full_a")
averageTimePausedMiddle_b = read.csv("output/AvgTimePausedMiddle/AvgTimePausedMiddle_full_b")
averageTimePausedMiddle_c = read.csv("output/AvgTimePausedMiddle/AvgTimePausedMiddle_full_c")

averageTimePausedMiddleModel_a = aov(AvgTimePausedFull ~ treatment, averageTimePausedFull_a)
averageTimePausedMiddleLME_a = lme(AvgTimePausedMiddle ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedMiddle_a)

averageTimePausedMiddleModel_b = aov(AvgTimePausedMiddle ~ treatment, averageTimePausedMiddle_b)
averageTimePausedMiddleLME_b = lme(AvgTimePausedMiddle ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedMiddle_b)

averageTimePausedMiddleModel_c = aov(AvgTimePausedMiddle ~ treatment, averageTimePausedMiddle_c)
averageTimePausedMiddleLME_c = lme(AvgTimePausedMiddle ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedMiddle_c)


png("averageTimePausedMiddle.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Average Time Paused Middle (a)')
summary(averageTimePausedMiddleModel_a)
summary(glht(averageTimePausedMiddleLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedMiddle ~ treatment, averageTimePausedMiddle_a)
ezPrecis(averageTimePausedMiddle_a)

writeLines("\n")

print('Average Time Paused Middle (b)')
summary(averageTimePausedMiddleModel_b)
summary(glht(averageTimePausedMiddleLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedMiddle ~ treatment, averageTimePausedMiddle_b)
ezPrecis(averageTimePausedMiddle_b)

writeLines("\n")

print('Average Time Paused Middle (c)')
summary(averageTimePausedMiddleModel_c)
summary(glht(averageTimePausedMiddleLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedMiddle ~ treatment, averageTimePausedMiddle_c)
ezPrecis(averageTimePausedMiddle_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Average Time Paused Corner (Full session)')
averageTimePausedCorner_a = read.csv("output/AvgTimePausedCorner/AvgTimePausedCorner_full_a")
averageTimePausedCorner_b = read.csv("output/AvgTimePausedCorner/AvgTimePausedCorner_full_b")
averageTimePausedCorner_c = read.csv("output/AvgTimePausedCorner/AvgTimePausedCorner_full_c")

averageTimePausedCornerModel_a = aov(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_a)
averageTimePausedCornerLME_a = lme(AvgTimePausedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedCorner_a)

averageTimePausedCornerModel_b = aov(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_b)
averageTimePausedCornerLME_b = lme(AvgTimePausedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedCorner_b)

averageTimePausedCornerModel_c = aov(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_c)
averageTimePausedCornerLME_c = lme(AvgTimePausedCorner ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedCorner_c)


png("averageTimePausedCorner.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Average Time Paused Corner (a)')
summary(averageTimePausedCornerModel_a)
summary(glht(averageTimePausedCornerLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_a)
ezPrecis(averageTimePausedCorner_a)

writeLines("\n")

print('Average Time Paused Corner (b)')
summary(averageTimePausedCornerModel_b)
summary(glht(averageTimePausedCornerLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_b)
ezPrecis(averageTimePausedCorner_b)

writeLines("\n")

print('Average Time Paused Corner (c)')
summary(averageTimePausedCornerModel_c)
summary(glht(averageTimePausedCornerLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedCorner ~ treatment, averageTimePausedCorner_c)
ezPrecis(averageTimePausedCorner_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Average Time Paused Edge (Full session)')
averageTimePausedEdge_a = read.csv("output/AvgTimePausedEdge/AvgTimePausedEdge_full_a")
averageTimePausedEdge_b = read.csv("output/AvgTimePausedEdge/AvgTimePausedEdge_full_b")
averageTimePausedEdge_c = read.csv("output/AvgTimePausedEdge/AvgTimePausedEdge_full_c")

averageTimePausedEdgeModel_a = aov(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_a)
averageTimePausedEdgeLME_a = lme(AvgTimePausedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedEdge_a)

averageTimePausedEdgeModel_b = aov(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_b)
averageTimePausedEdgeLME_b = lme(AvgTimePausedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedEdge_b)

averageTimePausedEdgeModel_c = aov(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_c)
averageTimePausedEdgeLME_c = lme(AvgTimePausedEdge ~ treatment, random = ~ 1 | crayfishid, data=averageTimePausedEdge_c)


png("averageTimePausedEdge.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Average Time Paused Edge (a)')
summary(averageTimePausedEdgeModel_a)
summary(glht(averageTimePausedEdgeLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_a)
ezPrecis(averageTimePausedEdge_a)

writeLines("\n")

print('Average Time Paused Edge (b)')
summary(averageTimePausedEdgeModel_b)
summary(glht(averageTimePausedEdgeLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_b)
ezPrecis(averageTimePausedEdge_b)

writeLines("\n")

print('Average Time Paused Edge (c)')
summary(averageTimePausedEdgeModel_c)
summary(glht(averageTimePausedEdgeLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(AvgTimePausedEdge ~ treatment, averageTimePausedEdge_c)
ezPrecis(averageTimePausedEdge_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Total Distance Traveled (Full session)')
totalDistAll_a = read.csv("output/TotalDistAll/TotalDistAll_full_a")
totalDistAll_b = read.csv("output/TotalDistAll/TotalDistAll_full_b")
totalDistAll_c = read.csv("output/TotalDistAll/TotalDistAll_full_c")

totalDistAllModel_a = aov(TotalDistAll ~ treatment, totalDistAll_a)
totalDistAllLME_a = lme(TotalDistAll ~ treatment, random = ~ 1 | crayfishid, data=totalDistAll_a)

totalDistAllModel_b = aov(TotalDistAll ~ treatment, totalDistAll_b)
totalDistAllLME_b = lme(TotalDistAll ~ treatment, random = ~ 1 | crayfishid, data=totalDistAll_b)

totalDistAllModel_c = aov(TotalDistAll ~ treatment, totalDistAll_c)
totalDistAllLME_c = lme(TotalDistAll ~ treatment, random = ~ 1 | crayfishid, data=totalDistAll_c)


png("totalDistTravled", width=1000, height=400)
par(mfrow=c(1, 3))

print('Total Distance Traveled (a)')
summary(totalDistAllModel_a)
summary(glht(totalDistAllLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistAll ~ treatment, totalDistAll_a)
ezPrecis(totalDistAll_a)

writeLines("\n")

print('Total Distance Traveled (b)')
summary(totalDistAllModel_b)
summary(glht(totalDistAllLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistAll ~ treatment, totalDistAll_b)
ezPrecis(totalDistAll_b)

writeLines("\n")

print('Total Distance Traveled (c)')
summary(totalDistAllModel_c)
summary(glht(totalDistAllLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistAll ~ treatment, totalDistAll_c)
ezPrecis(totalDistAll_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Total Distance Traveled Middle (Full session)')
totalDistMid_a = read.csv("output/TotalDistMid/TotalDistMid_full_a")
totalDistMid_b = read.csv("output/TotalDistMid/TotalDistMid_full_b")
totalDistMid_c = read.csv("output/TotalDistMid/TotalDistMid_full_c")

totalDistMidModel_a = aov(TotalDistMid ~ treatment, totalDistMid_a)
totalDistMidLME_a = lme(TotalDistMid ~ treatment, random = ~ 1 | crayfishid, data=totalDistMid_a)

totalDistMidModel_b = aov(TotalDistMid ~ treatment, totalDistMid_b)
totalDistMidLME_b = lme(TotalDistMid ~ treatment, random = ~ 1 | crayfishid, data=totalDistMid_b)

totalDistMidModel_c = aov(TotalDistMid ~ treatment, totalDistMid_c)
totalDistMidLME_c = lme(TotalDistMid ~ treatment, random = ~ 1 | crayfishid, data=totalDistMid_c)


png("totalDistMid.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Total Dist Middle (a)')
summary(totalDistMidModel_a)
summary(glht(totalDistMidLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistMid ~ treatment, totalDistMid_a)
ezPrecis(totalDistMid_a)

writeLines("\n")

print('Total Dist Middle (b)')
summary(totalDistMidModel_b)
summary(glht(totalDistMidLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistMid ~ treatment, totalDistMid_b)
ezPrecis(totalDistMid_b)

writeLines("\n")

print('Total Dist Middle (c)')
summary(totalDistMidModel_c)
summary(glht(totalDistMidLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistMid ~ treatment, totalDistMid_c)
ezPrecis(totalDistMid_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Total Distance Traveled Corner (Full session)')
totalDistCorner_a = read.csv("output/TotalDistCorner/TotalDistCorner_full_a")
totalDistCorner_b = read.csv("output/TotalDistCorner/TotalDistCorner_full_b")
totalDistCorner_c = read.csv("output/TotalDistCorner/TotalDistCorner_full_c")

totalDistCornerModel_a = aov(TotalDistCorner ~ treatment, totalDistCorner_a)
totalDistCornerLME_a = lme(TotalDistCorner ~ treatment, random = ~ 1 | crayfishid, data=totalDistCorner_a)

totalDistCornerModel_b = aov(TotalDistCorner ~ treatment, totalDistCorner_b)
totalDistCornerLME_b = lme(TotalDistCorner ~ treatment, random = ~ 1 | crayfishid, data=totalDistCorner_b)

totalDistCornerModel_c = aov(TotalDistCorner ~ treatment, totalDistCorner_c)
totalDistCornerLME_c = lme(TotalDistCorner ~ treatment, random = ~ 1 | crayfishid, data=totalDistCorner_c)


png("totalDistCorner.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Total Dist Corner (a)')
summary(totalDistCornerModel_a)
summary(glht(totalDistCornerLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistCorner ~ treatment, totalDistCorner_a)
ezPrecis(totalDistCorner_a)

writeLines("\n")

print('Total Dist Corner (b)')
summary(totalDistCornerModel_b)
summary(glht(totalDistCornerLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistCorner ~ treatment, totalDistCorner_b)
ezPrecis(totalDistCorner_b)

writeLines("\n")

print('Total Dist Corner (c)')
summary(totalDistCornerModel_c)
summary(glht(totalDistCornerLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistCorner ~ treatment, totalDistCorner_c)
ezPrecis(totalDistCorner_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")

print('Total Dist Edge (Full session)')
totalDistEdge_a = read.csv("output/TotalDistEdge/totalDistEdge_full_a")
totalDistEdge_b = read.csv("output/TotalDistEdge/totalDistEdge_full_b")
totalDistEdge_c = read.csv("output/TotalDistEdge/totalDistEdge_full_c")

totalDistEdgeModel_a = aov(TotalDistEdge ~ treatment, totalDistEdge_a)
totalDistEdgeLME_a = lme(TotalDistEdge ~ treatment, random = ~ 1 | crayfishid, data=totalDistEdge_a)

totalDistEdgeModel_b = aov(TotalDistEdge ~ treatment, totalDistEdge_b)
totalDistEdgeLME_b = lme(TotalDistEdge ~ treatment, random = ~ 1 | crayfishid, data=totalDistEdge_b)

totalDistEdgeModel_c = aov(TotalDistEdge ~ treatment, totalDistEdge_c)
totalDistEdgeLME_c = lme(TotalDistEdge ~ treatment, random = ~ 1 | crayfishid, data=totalDistEdge_c)


png("TotalDistEdge.png", width=1000, height=400)
par(mfrow=c(1, 3))

print('Total Dist Edge (a)')
summary(totalDistEdgeModel_a)
summary(glht(totalDistEdgeLME_a, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistEdge ~ treatment, totalDistEdge_a)
ezPrecis(totalDistEdge_a)

writeLines("\n")

print('Total Dist Edge (b)')
summary(totalDistEdgeModel_b)
summary(glht(totalDistEdgeLME_b, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistEdge ~ treatment, totalDistEdge_b)
ezPrecis(totalDistEdge_b)

writeLines("\n")

print('Total Dist Edge (c)')
summary(totalDistEdgeModel_c)
summary(glht(totalDistEdgeLME_c, linfct=mcp(treatment="Tukey")), test = adjusted(type = "bonferroni"))
plot(TotalDistEdge ~ treatment, totalDistEdge_c)
ezPrecis(totalDistEdge_c)

writeLines("\n")

dev.off()

print('__________________________________________')
writeLines("\n\n")
