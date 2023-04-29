def create_ascension_card(self, zerochan: bool = False, save: bool = False):
        '''
    
        creates ascension card
        
        '''
        char = self.data   

        
        img_url = None

        

        images = self.data.get('image', None)
        if images is not None:
            for img in images:
                if 'wish' in img.lower():
                    img_url = images[img]

        if zerochan:
            random_img = random_char_image(self.client.zerochan, self.name)
            if random_img is not None:
                img_url = random_img.url

        if img_url is not None:
            if zerochan:
                card =  ImageManipulation.create_image_card(self.name, img_url, False ,'Ascension and Talent Mats')
            else:
                card =  ImageManipulation.create_image_card(self.name, img_url, False ,'Ascension and Talent Mats',  -350, 95)
            max_item = 5
            start_x = card.size[0] // 2 - 250
            start_y = 250   
            end_x = start_x + (112*5)
            
            if len(self.data['ascension']['total']) != 0:                
                card = ImageManipulation.paste_cards(card, (start_x, start_y), (end_x,0), self.data['ascension']['total'])

           
            rows = len(self.data['ascension']['total']) // 5
            
           
            sum_cards = []

            cards_ = CharacterEXPFilter(90, card_exp_mat=['hw']).cards['cards']        
            sum_cards = add_cards(cards_)

            if len(self.data['talent_upgrade']['total']) != 0:
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          #      
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          # TRIPLE CROWN     
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          #
            
            end_x = start_x + (112 * (len(sum_cards) // 2))
            card = ImageManipulation.paste_cards(card, (start_x, (start_y + 122) +(122 * rows)), (end_x, 0), sum_cards)   
            

            if save:

                if not exists(self.client.images_path+self.name+"/"):
                    mkdir(self.client.images_path+self.name+"/")
                if not exists(self.client.images_path+self.name+"/ascension_talents/"):
                    mkdir(self.client.images_path+self.name+"/ascension_talents/")

                card.save(self.client.images_path+self.name+"/ascension_talents/ascension.png")

            return card