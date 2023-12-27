isAlive = True 
	if isAlive ==False:
		console.fill((0,0,0))
		restart_font = pygame.font.Font("freesansbold.ttf",50)
		restart_txt = restart_font.render("RESTART. Press R", True, (0,255,0))

		console.blit(restart_txt, (200,300))

		# Reset score, enemy_count
		score_val = 0
		enemy_count = random.randint(10,15)

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_R:
			run = True