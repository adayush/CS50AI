def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # find all neighbors of cell
        neighbors = self.find_all_neighbors(cell)

        # remove cells from neighbors set whose state is already known, and update mine count accordingly
        mine_count = count
        neighbors_to_remove = set()
        for neighbor in neighbors:
            if neighbor in self.mines:
                neighbors_to_remove.add(neighbor)
                mine_count -= 1
            if neighbor in self.safes:
                neighbors_to_remove.add(neighbor)
        neighbors -= neighbors_to_remove

        # add a new sentence to the AI's knowledge base
        new_sentence = Sentence(neighbors, mine_count)
        self.knowledge.append(new_sentence)

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        mines_to_mark = set()
        safes_to_mark = set()
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                mines_to_mark.add(mine)
            for safe in sentence.known_safes():
                safes_to_mark.add(safe)
        for mine in mines_to_mark:
            self.mark_mine(mine)
        for safe in safes_to_mark:
            self.mark_safe(safe)

        # Remove empty knowledge sentences
        sentences_to_remove = []
        for sentence in self.knowledge:
            if sentence.cells == set():
                sentences_to_remove.append(sentence)
        for sentence in sentences_to_remove:
            self.knowledge.remove(sentence)

        # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge (using subset method)
        knowledge_to_add = []
        for sentence in self.knowledge:
            if new_sentence.cells and sentence.cells != new_sentence.cells:
                if sentence.cells.issubset(new_sentence.cells):
                    knowledge_to_add.append(Sentence(new_sentence.cells-sentence.cells, new_sentence.count-sentence.count))
                if new_sentence.cells.issubset(sentence.cells):
                    knowledge_to_add.append(Sentence(sentence.cells-new_sentence.cells, sentence.count-new_sentence.count))
        self.knowledge += knowledge_to_add
        
        # print current knowledge base
        print("Number of sentenes in knowledge base: {}".format(len(self.knowledge)))
        for sentence in self.knowledge:
            print("{} = {}".format(sentence.cells, sentence.count))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        # no safe moves that haven't already been made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set(itertools.product(range(self.height), range(self.width)))
        possible_moves = list(all_moves - self.mines - self.moves_made)

        # no possible moves that are not known to be mines and that haven't already been made
        if not possible_moves:
            return None

        return random.choice(possible_moves)

    def find_all_neighbors(self, cell):
        """
        Returns a set of all neighbors for the cell (i, j)
        """
        i, j = cell[0], cell[1]
        neighbors = set()

        # neighbous above
        if (i-1 >= 0):
            neighbors.add((i-1, j))
            if (j-1 >= 0):
                neighbors.add((i-1, j-1))
            if (j+1 <= self.width-1):
                neighbors.add((i-1, j+1))

        # neighbors either side
        if (j-1 >= 0):
            neighbors.add((i, j-1))
        if (j+1 <= self.width-1):
            neighbors.add((i, j+1))
        
        # neighbors below
        if (i+1 <= self.height-1):
            neighbors.add((i+1, j))
            if (j-1 >= 0):
                neighbors.add((i+1, j-1))
            if (j+1 <= self.width-1):
                neighbors.add((i+1, j+1))
        
        return neighbors