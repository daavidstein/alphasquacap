library(tidyverse)
library(stringr)
library(here)
library(readxl)
library(lubridate)

# In case csv is lost: https://aspm.faa.gov/asqp/sys/Airport.asp
#https://aspmhelp.faa.gov/index.php/ASQP_Manual#Overview

standard_path <- here::here("data", "StandardReport.csv")
standard <- read_csv(standard_path)

# Removes stupid government tallies
standard <- standard %>%
  filter(!str_detect(Date, 'Sub-Total'))

# Converts Month-Year (JUN-13) to Date Format (2013-06-01)
standard$Date <- as.Date(sub("\\-", "01", standard$Date), "%b%d%y")

# Converts datetype to year string
standard$Date <- format(standard$Date, "%Y")

# ^^^ CSV CLEANED. Ignore above code if you use the cleaned csv!
# Sum up arrivals and arrivals on time per year for each airport
standard <- standard %>%
  group_by(Date, Facility) %>%
  summarise_at(
    .vars= vars(Actual_Arrivals, On_Time_Arrivals, Departure_Cancellations,
                Arrival_Cancellations, Departure_Diversions, Actual_Diversions,
                Delayed_Arrivals), 
    .funs =  sum)

# Create a proportion arrival on-time column
# Also gets rid of 2003, which is only half-filled
standard <- standard %>%
  mutate(Prop_On_Time = On_Time_Arrivals/Actual_Arrivals) %>%
  filter(Date != "2003")

# Joining with James' File
# Data downloaded from
t_path <- here::here("data", "yearly", "yearly_ops_all_airports.xlsx")
t <- read_excel(t_path, skip = 7)

t <- t %>% 
  select(1:2, 8) %>%
  mutate(
    #airport = ...1, 
    airport = X__1, 
         year = Year, 
         ops = Operations, 
         len = str_length(airport)) %>%
  filter(year > 1990 & year < 2019) %>%
  filter(len < 4) %>%
  select(airport, year, ops)

# Change column names with merge keys so that they match in both dfs:
standard <- plyr::rename(standard, c("Date"="year", "Facility"="airport"))

# Year needs to be numeric, not chr:
standard$year <- as.numeric(standard$year)

# Merging on airport and year
merged_df <- full_join(t, standard, by = c("airport", "year"))

#write.csv(merged_df, here::here("data", "yearly", "merged_ops_delay.csv"))