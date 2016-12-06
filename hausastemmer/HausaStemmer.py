# Copyright (C) 2013 Bimba Andrew Thomas, 2016 Linas Valiukas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details <http://www.gnu.org/licenses/>.


from .dict_lookup import ROOT_WORDS


# noinspection SpellCheckingInspection
class HausaStemmer:
    def __init__(self):

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0  # j is a general offset into the string
        self.h = 0  # h is a hyphen offset into the string

    @staticmethod
    def __check_dict(word):
        if word in ROOT_WORDS:
            return word
        else:
            return ''

    def __cons(self, i):
        """Returns True <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        else:
            return 1

            # if self.b[i] == 'y':
            #     if i == self.k0:
            #         return 1
            #     else:
            #         return (not self.cons(i - 1))
            # return 1

    def __hyphen(self, i):
        """Returns True <=> b[i] is a hyphen."""
        if self.b[i] == '-':
            self.h = i
            return 1
        else:
            return 0

    def __m(self):
        """Measures the number of consonant sequences between k0 and j. If c is a consonant sequence and v a vowel
        sequence, and <..> indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ...
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.__cons(i):
                break
            i += 1
        i += 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.__cons(i):
                    break
                i += 1
            i += 1
            n += 1
            while 1:
                if i > self.j:
                    return n
                if not self.__cons(i):
                    break
                i += 1
            i += 1

    def __has_single_hyphen(self):
        """Returns True <=> k0,...j contains single hyphen."""
        for i in range(self.k0, self.j + 1):
            if self.__hyphen(i):
                return 1
        return 0

    def __has_double_hyphen(self):
        """Returns True <=> k0,...j contains double hyphens."""
        count = 0
        for i in range(self.k0, self.j + 1):
            if self.__hyphen(i):
                count += 1
            if count == 2:
                return 1
        return 0

    def __is_duplicate(self):
        """Returns True <=> k0,...j contains duplicate words."""
        # if self.__has_single_hyphen:
        # for i in range(self.k0, self.j + 1):
        if self.h >= self.k0 + 4:
            if self.b[self.k0] == self.b[self.h + 1] and self.b[self.k0 + 1] == self.b[self.h + 2] and self.b[
                        self.k0 + 2] == self.b[self.h + 3] and self.b[self.k0 + 3] == self.b[self.h + 4]:
                return 1
            else:
                return 0
        else:
            return 0

    def __ends_with(self, s):
        """Returns True <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]:  # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k - length + 1:self.k + 1] != s:
            return 0
        self.j = self.k - length
        return 1

    def __starts_with(self, s):
        """Returns True <=> k0,...k starts with the string s."""
        length = len(s)
        if s[0] != self.b[self.k0]:  # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k0:self.k0 + length] != s:
            return 0
        self.j = length - 1
        return 1

    def __set_to(self, s):
        """Sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j + 1] + s + self.b[self.j + length + 1:]
        self.k = self.j + length

    def __r(self, s):
        if self.__m() >= 0 and len(self.b) > 4:
            self.__set_to(s)

    def __chk_center_combo_3(self):
        if (len(self.b) - self.k0) > 7:
            if (self.b[self.k0 + 2] + self.b[self.k0 + 3] + self.b[self.k0 + 4]) == (
                            self.b[self.k0 + 5] + self.b[self.k0 + 6] + self.b[self.k0 + 7]):
                return 1
            else:
                return 0

        return 0

    def __chk_start_combo_3(self):
        if (len(self.b) - self.k0) > 4:
            if self.__cons(self.k0) and not self.__cons(self.k0 + 1) and self.b[self.k0] == self.b[self.k0 + 2] == \
                    self.b[
                                self.k0 + 3]:
                return 1
            elif (len(self.b) - self.k0) > 6:
                if (self.b[self.k0] + self.b[self.k0 + 1] + self.b[self.k0 + 2]) == (
                                self.b[self.k0 + 3] + self.b[self.k0 + 4] + self.b[self.k0 + 5]):
                    return 1
                else:
                    return 0

        return 0

    def __chk_start_combo_2(self):
        if (len(self.b) - self.k0) > 6:
            if (self.b[self.k0] + self.b[self.k0 + 1]) == (self.b[self.k0 + 2] + self.b[self.k0 + 3]):
                return 1
            else:
                return 0
        else:
            return 0

    def __chk_end_combo_2(self):
        if (len(self.b) - self.k0) > 4:
            if (self.b[self.k - 1] + self.b[self.k]) == (self.b[self.k - 3] + self.b[self.k - 2]):
                return 1
            else:
                return 0
        else:
            return 0

    def __calc(self, s):
        """Replaces prefix (k-len(s)),...k based on the string s to the appropriate characters, by adding certain
        characters."""
        length = len(s)
        if length > (self.k - self.k0 + 1):
            return
        if self.__m() > 0:

            # Step 1c (ii)
            # m>1 for word starting with prefix "ma" and suffix "awa"
            # *cvcawa->*cvcv
            # mafadawa -> mafada (counselor)
            # madugawa -> madugu (chief of a caravan)
            if s == "awa":
                c = self.k - length
                v = self.k - length - 1
                vr = self.b[len(self.b) - length - 2]
                if self.__cons(c) and not self.__cons(v):
                    self.__r(vr)

            # Step 1e  (i)
            # m>1, *vwvchi -> *vwv e.g
            # Marowachi (greediness) -> rowa (to be greedy)
            elif s == "chi":
                v = self.k - length
                c = self.k - length - 1
                cr = self.b[len(self.b) - length - 2]
                vr = self.b[len(self.b) - length - 3]
                if cr == "w" and not self.__cons(v):
                    self.__r("")
                    self.k0 += 2

                    # Step 1e (ii)
                    # m>0, *cvuchi -> *cvuta e.g
                    # Mafauchi (butcher) -> fauta (slaughter)
                    # marubuchi ->  rubuta (write)
                    #
                elif self.b[v] == "u":
                    self.__r("ta")
                    self.k0 = 2

                    # m>0, *vcvchi -> *vcv e.g
                    # Marokachi (begging and beggar) -> roko (to beg)
                    # Matsorachi (cowardice) -> tsoro (fear)
                    #
                    # elif s=="chi":
                    #    c=self.k-length
                    #    v=self.k-length-1
                    #    vr=self.b[len(self.b)-length-2]
                if self.__cons(c) and not self.__cons(v):
                    self.__ends_with(self.b[v] + "chi")
                    self.__r(vr)
                    self.k0 += 2

                    # m>0, *nchi -> *nta e.g
                    # Makaranchi (scholar) -> karanta (to read)
                elif self.__cons(c + 1) and self.b[c + 1] == "n":
                    self.__r("ta")
                    self.k0 += 2

            # m>1 remove "suwa" with a preceding vowel and replace preceding
            # vowel with "a" i.e *cvsuwa -> *ca e.g
            # Tayesuwa (helping) ->   taya (to help)
            # Fitasuwa (coming out) ->   fita (to come out)
            elif s == "suwa":
                v = self.k - length
                if not self.__cons(v):
                    self.__ends_with(self.b[v] + "suwa")
                    self.__r("a")
                # m>1 remove "suwa" with a preceding consonant and add "e" i.e *csuwa -> *ce e.g
                # Rantsuwa (swearing, oath) -> rantse (to swear)
                else:
                    self.__ends_with("uwa")
                    self.__r("e")

            # m>1 remove "ta" and add the next preceding vowel
            #
            # makafta (blindness) -> makafa (blind man)
            # Gajerta (shortness) -> gajere (short)
            # Kasamta (uncleanness) ->  kasama (unclean, dirty person)
            # Kuturta (leprosy) -> Kuturu (to be leprous, leper)
            elif s == "ta":
                c = self.k - length
                v = self.k - length - 1
                vr = self.b[len(self.b) - length - 2]
                if not self.__cons(v) and self.__cons(c):
                    self.__r(vr)
                # m>1 remove "ta"
                # kariata (lying) -> karia (lie)
                # Mugunta (evil) -> mugun
                if not self.__cons(c):
                    self.__r("")

                if vr == "u":
                    self.__ends_with("uta")
                    self.__r("wa")
            # m>1 replace "oshi" with "i" if next word is a consonant else truncate "oshi" e.g
            # garwashoshi -> garwashi (burning charcoal)

            elif s == "oshi":
                c = self.k - length
                w = self.k0 + 1

                # ofisoshi -> ofis (office)
                if self.__cons(w):
                    self.__r("")

                # kusoshi -> kusa (nail)
                elif self.b[c] == "s":
                    self.__r("a")

                # garwashoshi -> garwashi (burning charcoal)
                elif self.__cons(c):
                    self.__r("i")

            # m>1 replace suffix "ye" with "ya" if remaining letters are repeated e.g
            #   mamaye -> mamaya (Attack suddenly; capture suddenly)
            elif s == "aye":
                cva = self.b[self.k0] + self.b[self.k0 + 1]
                cvb = self.b[self.k0 + 2] + self.b[self.k0 + 3]
                if cva == cvb:
                    self.__r("aya")
                # kwallaye -> kwallo
                elif self.b[self.k - 3] == self.b[self.k - 4]:
                    self.__r("o")

    def __step_1a(self):
        """Stem word reduplication and concrete nouns formed from prefixed particles and other nouns that use hyphens.

        Search for all hyphens and remove along with the attaching prepositions and word duplication if any.

        E.g.:

        * da-n-zunzua -> zunzua,
        * mai-gona -> gona,
        * ya-l-kano -> kano,
        * ba-haushe -> haushe,
        * chiye-chiye -> chiye,
        * guje-guje -> guje,
        * karanche-karanche -> karanche,
        * masu-aiki -> aiki,
        * masu-gona -> gona,
        * zanga-zangar -> zanga,
        * baya-bayan -> baya,
        * koke-kokensu -> koke,
        * tsince-tsincen -> tsince,
        * Na-Bakin-Kogi -> kogi,
        * Abi-n-chi (food) -> chi (to eat),
        * Abin-mamaki -> mamaki,
        * Abin-tsoro (a thing to fear) -> tsoro (to fear),
        * Wuri-n-rubutu (writing place) -> rubutu (to write),
        * da-n-makaranta -> makaranta

        Exception: Guje-guje (running) -> gudu (to run).
        """
        if self.__has_double_hyphen():
            self.k0 = self.h + 1
        elif self.__has_single_hyphen() and self.__is_duplicate():
            self.k = self.h - 1
        elif self.__has_single_hyphen():
            self.k0 = self.h + 1

        # m>1 rin->r
        #          teburin -> tebur (table)
        #
        elif self.__ends_with("rin") and len(self.b) > 6:
            self.__r("r")

        # and #m>1, replace repeated prefix e.g
        #   gagarumar-> garuma (a ring, a circular support)

        if self.__chk_start_combo_2():
            self.k0 = 2

            # m>1, replace prefix with consonant and vowel combination of form cvccv with cv where the all the c's are
            # same alphabet and the v's are same
            #
            # e.g:
            #   kakkausar -> kausar -> kausa (roughness)
            #   tattaunawar -> taunawar ->  tauna (chew, deal with principals)
            #   rarrabuwar ->  rabuwar -> rabu (separate)
            #
            #   and #m>1, replace repeated prefix e.g
            #   murmure-> mure (Become convalescent; recover from illness or bad times)

        if self.__chk_start_combo_3():
            self.k0 = 3
            # m>1 fen->
            #   kafafen -> kafa (leg)

        if self.__ends_with("fen") and len(self.b) > 6:
            self.__r("")

        # m>1 ir->i
        #   kungurmir -> kungurmi (The crown of the head)
        elif self.__ends_with("ir") and len(self.b) > 5:
            self.__r("i")

        # m>1 ar->a
        #   ranar -> rana
        #   kungiyar -> kungiya
        #   mutuwar->mutuwa
        elif self.__ends_with("ar") and len(self.b) > 4:
            self.__r("a")

        # m>1 Remove "n" at the end of the word e.g
        # Watan (month of) -> wata (month)
        # Mugun (from "mugunta" evil) -> mugu (bad, bad person)
        # Manyan -> manya (big)
        # Matsalolin-> Matsaloli (problem)
        if self.__ends_with("n") and len(self.b) > 4:
            self.__r("")

        # m>1 cce->
        #   kowacce -> kowa (table)
        if self.__ends_with("cce"):
            self.__r("")

    def __step_1b(self):
        """Stem concrete nouns formed from verb and prefixed with personal particles without hyphens:

            m>0             Remove "Mai"    e.g

        Maihalbi (marksman, hunter) -> halbi (to shoot)
        Maikoiyo (learner) -> koiyo (to learn)
        """
        if self.__starts_with("mai") and len(self.b) > 5:
            self.k0 = 3

    def __step_1c(self):
        """Stem Plural of compound nouns formed with prefix "ma" and suffix "ai"

        M>1 ai->a             e.g

        madaffai -> madaffa (kitchen) -> daffa (to cook)
        mahaukatai -> mahuakata (place of mad people)-> huakata (to be mad)
        mafautai -> mafauta (slaughter-place)-> fauta (to slaughter)
        makarantai -> makaranta (school)-> karanta (to read)
        mafutai -> mafuta (resting place)-> futa (t)

        * exceptions: madumkai -> madumki (tailor), mafarai -> mafari (beginning)
        """
        if self.__ends_with("ai") and len(self.b) > 4:
            self.__r("a")
            self.k0 = 2

            # M>1 for word starting with prefix "ma" and suffix "ra" replace suffix with "ri" and remove "ma"
            # e.g
            # mafara->mafari->fari (begin)
            #
        elif self.__ends_with("ra") and len(self.b) > 4:
            self.__r("ri")
            self.k0 = 2

            # M>1 for word starting with prefix "ma" and suffix "ka" replace suffix with "ki" and remove "ma"
            # e.g
            # madunka ->madunki (tailor) ->dunki (saw)
            #
        elif self.__ends_with("ka") and len(self.b) > 4:
            self.__r("ki")
            self.k0 = 2

            # M>1 for word starting with prefix "ma" and suffix "ta" or "fa" remove prefix "ma"
            # e.g
            # madaffa (kitchen) -> daffa (to cook)
            # mahuakata (place of mad people) ->huakata (to be mad)
            # mafauta (slaughter-place) -> fauta (to slaughter)
            # makaranta (school) i->karanta (to read)
            # mafuta (resting place) ->futa (to rest)
        elif self.__ends_with("ta") or self.__ends_with("fa") and len(self.b) > 4:
            self.k0 = 2

            # m>1, for word starting with prefix "ma" and suffix "awa"
            # *cvcawa->*cvcv
            # mafadawa -> mafada (counselor)
            # madugawa -> madugu (chief of a caravan)

        elif self.__ends_with("awa"):
            self.__calc("awa")

            # Stem Plural of compound nouns formed with prefix "ma" and has the suffix "ta"
            # m>1, ta->chi e.g
            # mafauta->mafauchi (butcher)
            # mahaukata->mahaukachi (madman)
            # marubuta ->marubuchi (writer)
            # makaranta->makaranchi (school)
            # mafuta->mafuchi (resting place)

        elif self.__ends_with("ta"):
            self.__r("chi")

            # Stem Abstract nouns formed from a verb or adjective with suffix "chi" and prefix "ma".
            # Search for words with suffix "chi" and prefix "ma" remove "ma" and perform the action indicated
            #        m>1, Remove "ma", e.g
            # Marowachi (greediness) -> rowa (to be greedy)
            # mahaukachi->hauka (madman)
            #

        elif self.__ends_with("chi"):
            self.__calc("chi")

            # Stem concrete nouns formed from verb with "Ma" prefixed and "Ya" suffixed
            # m>1, Remove "ma" and "ya", e.g
            # Mashaya (dinking place) -> sha

        elif self.__ends_with("ya"):
            self.__r("")
            self.k0 += 2

    def __step_2(self):

        # m>1 step 2 (i) change che -> tu "plural duplication"
        # Rubuche-rubuche (writing) -> rubutu (write)
        # Karanche-karanche (reading) ->karatu (read)
        if self.__ends_with("che"):
            self.__r("tu")

        # m>1 step 2 (ii)remove "suwa" with a preceding vowel and replace preceding vowel with "a" i.e *cvsuwa -> *ca
        # E.g.:
        # Tayesuwa (helping) ->   taya (to help)
        # Fitasuwa (coming out) ->   fita (to come out)
        elif self.__ends_with("suwa"):
            self.__calc("suwa")

        # Stem words with prefix "yan"
        #
        #       If word >=8, remove "yan", e.g
        #       Yankaba (children of destruction) -> kaba (name applied to pain)
        elif self.__starts_with("yan") and len(self.b) > 6:
            self.k0 += 3

        # m>1, remove "owa" with preceding vowel "o" and replace "o" with "a", e.g
        #       Tadowa (raising) ->   tada (to rise)
        elif self.__ends_with("owa"):
            self.__r("a")

        # m>1, remove "nchi"  and "ntaka", e.g
        #   baranchi, barantaka (service) -> bara (servant)
        #   daianchi, daiantaka (singleness) -> daia (one)
        #   gadonchi, gadontaka (inheritance) -> gado (inheritance)
        #
        # Exceptions:
        #   turanchi (what belongs to the white man) -> ture (white man's country),
        #   bakunchi
        #   bakuntaka (strangeness) -> bako (stranger),
        #   raganchi
        #   ragantaka (laziness) -> rago (idler, lazy person),
        #   sarkanchi
        #   sarkantaka(kingship) -> sariki (king),
        #   yaranchi
        #   yarantaka (youthfulness) -> yaro (boy)
        elif self.__ends_with("nchi") or self.__ends_with("ntaka"):
            self.__r("")

        # m>1, remove "nci", e.g
        #   fuskanci(to face) -> fuska (face)
        elif self.__ends_with("nci") and len(self.b) > 6:
            self.__r("")

        # m>1, remove "nni", e.g
        #   wasanni(games) -> wasa (game)
        elif self.__ends_with("nni") and len(self.b) > 6:
            self.__r("")

        # m>1, remove "nsa" or "nsu", e.g
        #   wasansa(his play) -> wasa (play)
        #   kurensu (their limt)->kure(limit)
        #   motocinsu (their car) -> motoci (cars)
        elif self.__ends_with("nsa") or self.__ends_with("nsu"):
            self.__r("")

        # m>1, remove "nshi","nka", or  "nku" e.g
        #   wasanshi (his play) -> wasa (play)
        #   karyanka (you are lied)->karya(lie)
        #   karyanku -> karya(lie)
        elif self.__ends_with("nshi") or self.__ends_with("nka") or self.__ends_with("nku"):
            self.__r("")

        # m>1, replace suffix "uka" with "e" e.g
        # kauyuka->kauye
        # karnuka ->kare

        elif len(self.b) > 5 and self.__ends_with("uka"):
            if self.__cons(self.k - 3) and self.__cons(self.k - 4):
                # self.b= self.b[self.k0:self.k-3]
                self.__ends_with(self.b[self.k - 3] + "uka")
                self.__r("e")
            else:
                self.__r("e")

                #       m>1, replace suffix "nta" e.g
                #       jagoranta -> jagora (blind person's guide)
                #       mugunta -> mugu (wicked)
        elif self.__ends_with("nta") and len(self.b) > 5:
            self.__r("")

        # m>1, remove "chi" and "taka" for words with preceding consonant "m" and replace with "i", e.g
        #   zarumchi, zarumtaka (bravery) -> zarumi (brave man)
        #
        elif self.__ends_with("mchi") or self.__ends_with("mtaka"):
            self.__r("i")

        # m>1 remove "ta" and replace preceding "u" with "wa" if preceding consonant is not w. If "w" replace with "o"
        # e.g
        # Chiwuta (sickness) -> chiwo (sick)
        # wauta (folly) -> wawa (fool)
        # fauta (slaughter) ->fawa (to slaughter)
        # bauta (slavery) -> bawa (slave
        # * exception sarauta (kingdom) -> sarki (king) not sarawa
        if self.__ends_with("ta"):
            self.__calc("ta")

        # m>1 nna->n:
        #   tukunna -> tukun (already)
        elif self.__ends_with("nna"):
            self.__r("n")

    def __step_3(self):
        # m>1 replace "obi" with "a", e.g:
        #   gabobi->gaba (front, breast)
        #   gambobi -> gamba (grass, a kind of hoe)
        #   goribobi -> goriba (a palm fruit)
        #   habobi-> haba (chin)
        if self.__ends_with("obi"):
            self.__r("a")

        # m>1 replace "ochi" with "a", e.g:
        #   batochi -> bata (small box made of skin)
        #   hanchochi->hanchi (nose)
        elif self.__ends_with("ochi"):
            self.__r("a")

        # m>1 replace "odi" with "a", e.g:
        #    Adodi -> ado (splendor)
        #    kafadodi->kafada (shoulder)
        #    fadodi->fada (chief's court)
        #    gadodi->gado (inheritence)
        elif self.__ends_with("odi"):
            self.__r("a")

        # m>1 replace "ofi" with "a", e.g:
        #    kofofi->kofa (door)
        #    aljifofi->aljifa (pocket)
        elif self.__ends_with("ofi"):
            self.__r("a")

        # m>1 replace "oji" with "a", e.g:
        #    sojoji -> soja (soldier)
        elif self.__ends_with("oji"):
            self.__r("a")

        # m>1 replace "ogi" with "a", e.g:
        #    bindigogi->bindiga (gun)
        #    gugogi->guga (bucket)
        #    kangogi -> kango (ruin)
        #    rigogi->riga (cloth)
        #    dangogi->danga (fence)
        elif self.__ends_with("ogi"):
            self.__r("a")

        # m>1 replace "oli" with "a", e.g:
        #    fitiloli->fitila (lamp)
        #    Matsaloli-> Matsala (problem)
        elif self.__ends_with("oli"):
            self.__r("a")

        # m>1 replace "oki" with "a", e.g:
        #
        #   hiskoki->hiska (wind)
        #   tsumoki -> tsuma (rag)
        #
        # Exception:
        #   tafarkoki->tafariki (method),
        #   dukoki->dukia (riches)
        elif self.__ends_with("oki"):
            self.__r("a")

        # m>1 replace "omi" with "i", e.g.:
        #    takalmomi->takalmi (shoe)
        #    alamomi ->alama(sign)
        elif self.__ends_with("omi"):
            self.__r("i")

        # m>1 replace "ori" with "i" e.g.:
        #    irori->iri (kind)
        elif self.__ends_with("ori"):
            self.__r("i")

        # m>1 replace "osi" with "a", e.g:
        #    yasosi->yatsa
        #    albasosi->albasa (onion)
        elif self.__ends_with("osi"):
            self.__r("a")

        # m>1 replace "oti" with "a", e.g.:
        #   likitoti->likita (doctor)
        elif self.__ends_with("oti"):
            self.__r("a")

        # m>1 replace "oshi" with "i" if next word is a consonant else truncate "oshi", e.g.:
        #    garwashoshi -> garwashi (burning charcoal)
        #    ofisoshi -> ofis (office)
        elif self.__ends_with("oshi"):
            self.__calc("oshi")

        # m>1 replace "owi" with "a"
        elif self.__ends_with("owi"):
            self.__r("a")

        # m>1 replace "oyi" with "a", e.g.:
        #    chibiyoyi->chibia (navel)
        #    doiyoyi -> doiya (yam)
        elif self.__ends_with("oyi"):
            self.__r("a")

    def __step_4(self, lookup=True):

        # m>1 ai->i:
        #    abokai -> aboki (friend)
        #    alkalai -> alkali   (judge)
        # Exception: barai -> barao (thief)
        if self.__ends_with("ai") and len(self.b) > 4:
            self.__r("i")

        # m>1, replace suffix "ri" with "ra", e.g.:
        #   yunkuri -> yunkura (put forth effort)
        #
        elif self.__ends_with("ri"):
            self.__r("ra")

        # m>1, replace suffix una -> a, e.g.:
        #    shaiduna -> shaida (witness)
        #    aljifuna -> aljifa (pocket)
        #    fatuna -> fata (skin)
        #    ganguna -> ganga (drum)
        # Exception: anguna -> ango (bridegroom), bantuna -> bante (towel)
        elif self.__ends_with("una"):
            self.__r("a")

        # ana -> a:
        #   jakadana-> jakada (messenger)
        elif self.__ends_with("ana"):
            self.__r("a")

        # m>1 replace suffix "ye" with "ya" if remaining letters are repeated, e.g.:
        #   mamaye -> mamaya (Attack suddenly; capture suddenly)
        elif self.__ends_with("aye"):
            self.__calc("aye")

        # m>1 remove suffix "ye", e.g.:
        #   bokaye -> boka (wizard)
        #   gataye -> gata(spy)
        #   kuraye->kura (hyena)
        #   gimbaye->gimba (seed used as a bead)
        #   chiye-chiye (eating) -> chi (to eat)
        #   shaye-shaye (drinking) -> sha(to drink)
        #
        # Exceptions:
        #   Koye-koye (learning) -> koyo (to learn),
        #   ragaye -> rago (idler)
        #   bebaye -> bebe (dumb person)
        #   buzaye -> buzu (half hausa, half tawarek)
        #   kifaye -> kifi (fish)
        if self.__ends_with("ye") and len(self.b) > 4:
            self.__r("")

        # m>1 nsa->
        #   gwamnatinsa (his government)  -> gwamnati  (government)
        if self.__ends_with("nsa") and len(self.b) > 6:
            self.__r("")

        # m>1 rer->ra:
        #   allurer -> allura (injection, needle)
        if self.__ends_with("rer") and len(self.b) > 4:
            self.__r("ra")

        # m>1 replace "shi" with "s", e.g.:
        #   ofishi -> ofis (ofis)
        elif self.__ends_with("shi"):
            self.__r("s")

        # m>1, replace suffix "*sa" with "shi" where * is a vowel, e.g.:
        #   kausa -> kaushi (roughness)
        #   matasa (youths) -> matashi (youth)
        if self.__ends_with("sa") and not self.__cons(self.k - 2):
            self.__r("shi")

        # Plural of compound nouns formed with particles: m>2 remove "wa"
        #   hausawa -> hausa (hausa person)
        #   godewa -> gode (appreciation)
        #   Chewa (saying) ->  che (to say)
        #   Dubawa (looking) ->   duba (to look at)
        #   Mutuwa (Death) -> mutu (to die)
        #
        # Exception:
        #   larabawa -> ba-larabe (arab),
        #   turawa -> ba-ture (European),
        #   Tsohuwa (old woman) -> tsoho (old)
        if self.__ends_with("wa") and len(self.b) > 5:
            self.__r("")

        # m>1, remove suffix "ke". e.g.:
        #   wukake->wuka (knife)
        if self.__ends_with("ke") and len(self.b) > 5:
            self.__r("")

        # m>1, remove suffix "ni", e.g.:
        #   kakani  -> kaka (grandfather, ancestors)
        #   wadani -> wada (dwarf)
        #   garani -> gara (white ant, termite)
        #   watani -> wata (month)
        if self.__ends_with("ni") and len(self.b) > 4:
            self.__r("")

        # m>1, replace suffix "nu" with "ni", e.g:
        #   aljanu -> aljani (demon)
        elif self.__ends_with("nu"):
            self.__r("ni")

        # m>1, remove suffix "nni", e.g.:
        #   unguwanni -> unguwa (section, town, village)
        if self.__ends_with("nni") and len(self.b) > 5:
            self.__r("")

        # m>1, replace suffix "ku" with "ki", e.g.:
        #   maraku -> maraki (calf)
        elif self.__ends_with("ku") and len(self.b) > 4:
            self.__r("ki")

        # m>1, remove suffix "ki", e.g.:
        #   gonaki -> gona (farm)
        #   kwanaki -> kwana (day of 24 hours)
        #   ranaki -> rana (day)
        if self.__ends_with("ki") and len(self.b) > 5:
            self.__r("")

        # m>1, remove suffix "nda", e.g.:
        #   yayinda -> yayi (period)
        elif self.__ends_with("nda") and len(self.b) > 5:
            self.__r("")

        # m>1, replace suffix "mci" with "mta", e.g.:
        #   fahimci -> fahimta (understand)
        elif self.__ends_with("mci"):
            self.__r("mta")

        # m>1, remove suffix "nmu", e.g.:
        #   motocinmu (our car) -> motoci (cars)
        elif self.__ends_with("nmu") and len(self.b) > 5:
            self.__r("")

        # m>1, remove suffix "ci", e.g.:
        #   arewaci -> arewa (north)
        #   gayyaci -> gayya (to ask for assistance)
        if self.__ends_with("ci") and len(self.b) > 5:
            self.__r("")

        # m>1, replace suffix "ru" with "ra", e.g.:
        #   dakaru -> dakara (bodyguard)
        #   zakaru -> zakara (cock)
        elif self.__ends_with("ru") and len(self.b) > 5:
            self.__r("ra")

        # m>1, replace suffix "taka" e.g "taki"
        #   mataka (steps) -> mataki (step)
        elif self.__ends_with("taka"):
            self.__r("taki")

        # m>1, remove suffix "gu", e.g.:
        #   balagagu (young adults) ->  balagaga (young adult)
        elif self.__ends_with("gu") and len(self.b) > 5:
            self.__r("")

        # m>1, replace suffix "ilu" with "il", e.g.:
        #   afrilu -> afril (april)
        elif self.__ends_with("ilu") and len(self.b) > 5:
            self.__r("il")

        # m>1, replace suffix "rko" with "ri", e.g.:
        #   farko (beginning) -> fara (begin)
        elif self.__ends_with("rko"):
            self.__r("ra")

        # m>1, replace suffix "ko" with "ka", e.g.:
        #   binciko (inquiries) ->  bincika (search or inquire)
        elif self.__ends_with("ko"):
            self.__r("ka")

        # m>1, replace suffix "ina" with "i", e.g:
        #   hankalina->  hankali (careful)
        #   raina -> rai (life)
        elif self.__ends_with("ina"):
            self.__r("i")

        # m>1, replace suffix "yu" with "re", e.g.:
        #   marayu -> marare (orphan)
        elif self.__ends_with("yu"):
            self.__r("re")

        # m>1, replace prefix "udda" with "adi", e.g.:
        #   sharudda ->  Sharadi (An Agreement, agreement)
        elif self.__ends_with("udda"):
            self.__r("adi")

        # m>1, if word starts with "m" and ends with "ma" replace suffix "ma" with "mi", e.g.:
        #   muhimma -> muhimmi (big, important)
        elif self.__starts_with("m") and self.__ends_with("ma") and len(self.b) > 5:
            self.__r("mi")

        # m>1, remove "tar" if the resulting letters form a root word, e.g.:
        #   tarwatsa (scattering) -> watsa (to scatter)
        elif self.__starts_with("tar"):
            self.k0 = 3
            # Check Dictionary
            if lookup:
                word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
                if word_dict == '':
                    self.k0 = 0

                    # m>1 remove prefix "tsat" or "tsatt" depending on word
                    # tsattsaga (seperate) -> tsaga (cut, divide, rip, split)
                    # tsattsaura (undeveloped) -> saura (remain)

        elif self.__starts_with("tsatt"):
            self.k0 = 4
            # Check Dictionary
            if lookup:
                word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
                if word_dict == '':
                    self.k0 = 5
                    word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
                    if word_dict == '':
                        self.k0 = 0

                        # and #m>1, replace repeated prefix e.g
                        # gagarumar-> garuma (a ring, a circular support)

        # truncate word with duplicative suffix e.g abubu->abu
        if self.__chk_end_combo_2():
            self.k -= 2

        # m>1 truncate word with duplicative circumfix e.g littattafi->littafi
        if self.__chk_center_combo_3():
            self.b = self.b[self.k0:self.k0 + 2] + self.b[self.k0 + 5:self.k + 1]

    def stem(self, p, lookup=True):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed is from p[i] to p[j] inclusive. Typically i
        is zero and j is the offset to the last character of a string, (p[j+1] == '\0'). The stemmer adjusts the
        characters p[i] ... p[j] and returns the new end-point of the string, k. Stemming never increases word length,
        so i <= k <= j. To turn the stemmer into a module, declare 'stem' as extern, and delete the remainder of this
        file."""

        p = p.strip()

        # FIXME L.V.: sample scripts pass the words as lower-case, should this always be done?
        p = p.lower()

        # copy the parameters into statics
        self.b = p
        self.k = len(p) - 1
        self.j = self.k
        self.k0 = 0
        if self.k <= self.k0 + 1:
            return self.b  # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        # Step 1a
        self.__step_1a()

        # Check Dictionary
        if lookup:
            word_dict = self.__check_dict(self.b)
            if word_dict != '':
                return word_dict

        # Step 1b
        self.__step_1b()

        if lookup:
            # Check Dictionary
            word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
            if word_dict != '':
                return word_dict

        if self.__starts_with("ma"):
            # Step 1c
            self.__step_1c()

        # Check Dictionary
        if lookup:
            word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
            if word_dict != '':
                return word_dict

        # Step 2
        self.__step_2()

        # Check Dictionary
        if lookup:
            word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
            if word_dict != '':
                return word_dict

        if len(self.b) > 6:
            # Step 3
            self.__step_3()

        # Check Dictionary
        if lookup:
            word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
            if word_dict != '':
                return word_dict

        # Step 4
        self.__step_4(lookup=lookup)

        # Check Dictionary
        if lookup:
            word_dict = self.__check_dict(self.b[self.k0:self.k + 1])
            if word_dict != '':
                return word_dict

        return self.b[self.k0:self.k + 1]
