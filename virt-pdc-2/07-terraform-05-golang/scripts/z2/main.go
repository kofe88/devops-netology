package main

import "fmt"

func main() {
	v_position := 0
	v_x := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17,}
	v_min := v_x[0]

	for i, v_temp := range v_x {
		if v_min > v_temp {
			v_min = v_temp
			v_position = i
		}
	}

	fmt.Println("Element: ", v_min, " Position: ", v_position)
}
