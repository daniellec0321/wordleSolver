#!/usr/bin/python3

class Word:

		# constructor
        def __init__(self, string_in, common_map):
            self.string = string_in

        #def find_scores(common_map):

			# finding the info rank of a word
            the_score = 0
            
            # set to keep track of what words we have encountered
            the_letters = set()

            for x in string_in:

                # make sure x is NOT in set, then add to score
                if not (x in the_letters):

                    the_letters.add(x)
			
                    if x == 'a':
                        the_score += 9.24

                    elif x == 'b':
                        the_score += 2.51

                    elif x == 'c':
                        the_score += 3.12

                    elif x == 'd':
                        the_score += 3.78

                    elif x == 'e':
                        the_score += 10.28

                    elif x == 'f':
                        the_score += 1.72

                    elif x == 'g':
                        the_score += 2.53

                    elif x == 'h':
                        the_score += 2.71

                    elif x == 'i':
                        the_score += 5.8

                    elif x == 'j':
                        the_score += 0.45

                    elif x == 'k':
                        the_score += 2.31

                    elif x == 'l':
                        the_score += 5.2

                    elif x == 'm':
                        the_score += 3.05

                    elif x == 'n':
                        the_score += 4.55

                    elif x == 'o':
                        the_score += 6.84

                    elif x == 'p':
                        the_score += 3.11

                    elif x == 'q':
                        the_score += 0.17

                    elif x == 'r':
                        the_score += 6.42

                    elif x == 's':
                        the_score += 10.27

                    elif x == 't':
                        the_score += 5.09

                    elif x == 'u':
                        the_score += 3.87

                    elif x == 'v':
                        the_score += 1.07

                    elif x == 'w':
                        the_score += 1.6

                    elif x == 'x':
                        the_score += 0.44

                    elif x == 'y':
                        the_score += 3.2

                    elif x == 'z':
                        the_score += 0.67

            self.info_rank = the_score

            # finding the commonality of a word
            if string_in in common_map:
                self.common_rank = common_map[string_in]
            else:
                self.common_rank = len(common_map)
