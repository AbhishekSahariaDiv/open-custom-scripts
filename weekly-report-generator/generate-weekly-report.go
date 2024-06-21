package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	projects := make(map[string][]string)
	projectTimes := make(map[string]int)

	var currentProject string
	for scanner.Scan() {
		line := scanner.Text()

		if strings.HasPrefix(line, "・[P") {
			projectRegex := regexp.MustCompile(`\[P\d+\]`)
			currentProject = projectRegex.FindString(line)

			timeRegex := regexp.MustCompile(`\((\d+)h(\d+)?\)|\((\d+)m\)`)
			timeMatches := timeRegex.FindStringSubmatch(line)
			if len(timeMatches) > 0 {
				if timeMatches[1] != "" {
					hours, _ := strconv.Atoi(timeMatches[1])
					minutes := 0
					if timeMatches[2] != "" {
						minutes, _ = strconv.Atoi(timeMatches[2])
					}
					projectTimes[currentProject] += hours*60 + minutes
				} else if timeMatches[3] != "" {
					minutes, _ := strconv.Atoi(timeMatches[3])
					projectTimes[currentProject] += minutes
				}
			}

			if _, ok := projects[currentProject]; !ok {
				projects[currentProject] = []string{line}
			}
		} else if strings.HasPrefix(line, "  - ") {
			if tasks, ok := projects[currentProject]; ok {
				if !contains(tasks[1:], line) {
					projects[currentProject] = append(tasks, line)
				}
			}
		}
	}

	totalTime := 0
	for projectID, tasks := range projects {
		projectTime := projectTimes[projectID]
		totalTime += projectTime

		hours := projectTime / 60
		minutes := projectTime % 60

		timeString := fmt.Sprintf("(%dh%02dm)", hours, minutes)
		projectLine := tasks[0]
		updatedProjectLine := regexp.MustCompile(`\(\d+[hm]\d*\)`).ReplaceAllString(projectLine, timeString)

		fmt.Println(updatedProjectLine)
		for _, task := range tasks[1:] {
			fmt.Println(task)
		}

		fmt.Println()
	}

	totalHours := totalTime / 60
	totalMinutes := totalTime % 60
	fmt.Printf("Total time: %dh%02dm\n", totalHours, totalMinutes)
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}
