package novels.annotators;

import java.util.Map;
import java.util.TreeMap;

import java.lang.Character;

import novels.Book;
import novels.Quotation;
import novels.Token;
import novels.entities.PronounAntecedent;
import novels.annotators.PhraseAnnotator;
import novels.entities.NP;
import novels.Dictionaries;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

import java.util.*;
/**
 * Attribute quotes to speakers
 * 
 * @author dbamman
 * 
 */
public class QuotationAnnotator {

	public void findQuotations(Book book, Dictionaries dicts) {

		// Add "I" as possible speaker
		for (Token token : book.tokens) {
			if (token.pos.startsWith("PRP") && (token.lemma.equals("I"))) {
				PronounAntecedent pronoun = new PronounAntecedent(
						token.tokenId, 0);
				book.animateEntities.put(token.tokenId, pronoun);
			}
		}

		TreeMap<Integer, Quotation> quotations;

		int start = 0;
		int end = 0;

		quotations = Maps.newTreeMap();

		int doubleQuotes = 0;
		int singleQuotes = 0;
		for (Token token : book.tokens) {
			if (token.lemma.equals("``")) {
				doubleQuotes++;
			} else if (token.lemma.equals("`")) {
				singleQuotes++;
			}
		}

		boolean usesSingleQuotes = false;
		if (singleQuotes > doubleQuotes) {
			usesSingleQuotes = true;
		}

		boolean open = false;

		if (usesSingleQuotes) {

			Token previousToken = null;

			// fixes a problem with single quotes before "I" not being recognized as open quotes
			for (int i = 0; i < book.tokens.size(); i++) {
				Token token = book.tokens.get(i);
				if (token.original.equals("'")) {
					if (!previousToken.whitespaceAfter.equals("")) {
						token.lemma="`";
						token.word="`";
						token.pos="``";
					}
				}
				previousToken=token;
			}


			previousToken = null;

			for (int i = 0; i < book.tokens.size(); i++) {
				Token token = book.tokens.get(i);
				if (token.lemma.equals("`")) {

					if (!previousToken.whitespaceAfter.equals("")) {
						open = true;
						start = token.tokenId;
					}
				} else if (token.lemma.equals("'")) {
					end = token.tokenId;

					if (start > -1 && open) {
						Quotation quote = new Quotation(start, end,
								token.sentenceID);
						quote.p = token.p; // **
						quotations.put(start, quote);
					}
					start = -1;

					open = false;

				}
				previousToken = token;

			}
		} else {
			for (Token token : book.tokens) {
				if (token.lemma.equals("``")) {
					open = true;
					start = token.tokenId;
				} else if (token.lemma.equals("''")) {
					end = token.tokenId;

					if (start > -1 && open) {
						Quotation quote = new Quotation(start, end,
								token.sentenceID);
						quote.p = token.p; // **
						quotations.put(start, quote);
					}
					start = -1;

					open = false;
				}
			}
		}

		for (Token token : book.tokens) {
			token.quotation = "O";
		}
		for (int qstart : quotations.keySet()) {
			Quotation quotation = quotations.get(qstart);
			book.tokens.get(quotation.start).quotation = "B-QUOTE";
			for (int s = quotation.start+1; s <= quotation.end; s++) {
				book.tokens.get(s).quotation = "I-QUOTE";
			}
		}

		// // combine quotations than span multiple sentences
		// HashSet<Integer> rem = Sets.newHashSet();
		// for (Quotation quote : quotations.values()) {
		// Map.Entry<Integer, Quotation> map = quotations
		// .ceilingEntry(quote.sentenceId + 1);
		// if (map != null) {
		// Quotation next = map.getValue();
		// Token endTok = book.tokens.get(quote.end);
		// Token startTok = book.tokens.get(next.start);
		// if (endTok.sentenceID == startTok.sentenceID) {
		// next.start = quote.start;
		// rem.add(quote.sentenceId);
		// }
		//
		// }
		// }
		// for (Integer i : rem) {
		// quotations.remove(i);
		// }

		// find speakers within the span of the sentence itself, e.g.: `` ...
		// ,'' said Darcy , `` ... ''
		
		//for (Quotation quote : quotations.values()) {
		
		//	for (int i = quote.start; i <= quote.end; i++) {
		//		Token token = book.tokens.get(i);
		//		if (book.animateEntities.containsKey(i) && token.quotation == false && !token.pos.equals("PRP$")) {
		//			quote.attributionId = i;
		//			break;
		//		}
		//		
		//	}
		//}

		// span left until the previous sentence

		for (Quotation quote : quotations.values()) {
		
		
			if (quote.attributionId != 0) {
			
				continue;
			}
			
						

			int quoteSentence = book.tokens.get(quote.start).sentenceID;
			int i = quote.start;
			int currentSentence = quoteSentence;
			while (quoteSentence == currentSentence && i >= 0) {

				Token token = book.tokens.get(i);
				currentSentence = token.sentenceID;
				if (quoteSentence != currentSentence)
					break;
				if (book.animateEntities.containsKey(i)
						&& token.quotation.equals("O")
						&& !token.pos.equals("PRP$")) {
					quote.attributionId = i;
					//System.out.println("1 " + quote.sentenceId + " " + quote.attributionId);
					break;
				}
				i--;
			}
		}

		// span right until the next sentence
		for (Quotation quote : quotations.values()) {
		

			if (quote.attributionId != 0) {		

				continue;
			}

			//int p = quote.p
			int quoteSentence = book.tokens.get(quote.end).sentenceID;
			int i = quote.end;
			int currentSentence = quoteSentence;			
			while (quoteSentence == currentSentence && i < book.tokens.size()) {
			//while (currentSentence - quoteSentence < 2  && i < book.tokens.size()) {

				Token token = book.tokens.get(i);
				currentSentence = token.sentenceID;
				//if (!(currentSentence - quoteSentence < 2))
				if (quoteSentence != currentSentence)
					break;
				if (book.animateEntities.containsKey(i)
						&& token.quotation.equals("O")
						&& !token.pos.equals("PRP$")) {
					quote.attributionId = i;
					//System.out.println("2 " + quote.sentenceId + " " + quote.attributionId);
					break;
				}
				i++;
			}
		}

		// span left until the previous quote or a hard punctuation
		for (Quotation quote : quotations.values()) {

			if (quote.attributionId != 0) {
			

				continue;
			}

			int p = quote.p;

			Map.Entry<Integer, Quotation> map = quotations
					.floorEntry(quote.start - 1);
			if (map != null) {
				Quotation previous = map.getValue();
				for (int i = quote.start; i > previous.end && i >= 0; i--) {
					Token token = book.tokens.get(i);
					if (token.word.matches("[\\.!;\\?]")) {
						break;
					}
					if (token.p != p)
						break;
					if (book.animateEntities.containsKey(i)
							&& token.quotation.equals("O")
							&& !token.pos.equals("PRP$")) {
						quote.attributionId = i;
						//System.out.println("3 " + quote.sentenceId + " " + quote.attributionId);
						break;
					}					
			
				}
			}
		}

		// span right until the next quote or a hard punctuation
		for (Quotation quote : quotations.values()) {


			if (quote.attributionId != 0) {			

				continue;
			}

			int p = quote.p;
			Map.Entry<Integer, Quotation> map = quotations
					.ceilingEntry(quote.start + 1);
			if (map != null) {
				Quotation next = map.getValue();
				for (int i = quote.end; i < next.start && i < book.tokens.size(); i++) {
					Token token = book.tokens.get(i);
					if (token.word.matches("[\\.!;:\\?]")) {
						break;
					}
					if (token.p != p)
						break;
					if (book.animateEntities.containsKey(i)
							&& token.quotation.equals("O")
							&& !token.pos.equals("PRP$")) {
						quote.attributionId = i;
						//System.out.println("4 " + quote.sentenceId + " " + quote.attributionId);
						break;
					}

				}
			}
		}

		//scanning into previous sentence 
	/*	
		for (Quotation quote : quotations.values()) {

			if (quote.attributionId != 0) {
			

				continue;
			}

			PhraseAnnotator ph = new PhraseAnnotator();
			int quoteSentence = book.tokens.get(quote.end).sentenceID;
			int i = quote.start;
			Token nextWord = book.tokens.get(quote.end + 1);
				
			if (Character.isLowerCase(nextWord.word.charAt(0)))
			{
				System.out.println((quote.end + 1) + " " + nextWord.word + " " + nextWord.word.charAt(0));
				continue;
			}			
			int currentSentence = quoteSentence;
			
			Map.Entry<Integer, Quotation> map = quotations.floorEntry(quote.start - 1);
			if (map != null) {
				System.out.println("MAP NOTT NULL");
				Quotation previous = map.getValue();
				int prevId = previous.attributionId;

				while ((quoteSentence - currentSentence) <= 1 && i >= 0) {
					
					
					Token token = book.tokens.get(i);
				
					currentSentence = token.sentenceID;

					if ((quoteSentence - currentSentence) > 1)
						break;		
					
					if ((i - prevId) < 2 && (i-prevId) >= 0 || (prevId - i) < 2 && (prevId - i) >= 0){
						System.out.println("BREKING " + i + " " + prevId);
						break;
					}//if (!((i - prevId) < 2|| (prevId - i) < 2)){						
						if ((token.pos.equals("PRP") || token.pos.startsWith("NN")) && token.deprel.equals("nsubj") && token.quotation == false && token.ner.equals("PERSON")){
							
						
							quote.attributionId = i;
					
							//PhraseAnnotator ph = new PhraseAnnotator();
							//NP phrase = ph.getPhrase(token.tokenId, book, dicts);
							//book.animateEntities.put(token.tokenId, phrase);
							System.out.println("5a " + quote.sentenceId + " " + quote.attributionId);
							break;
						}
						else if ((token.pos.equals("PRP") || token.pos.startsWith("NN")) && token.deprel.equals("nsubj") && token.quotation == false){
							//if ((i - prevId) < 2|| (prevId - i) < 2)
							//	continue;						
							//System.out.println(token.pos + " " + token.deprel + " " + token.quotation + " " + token.ner + " " + i);
							quote.attributionId = i;
					
							//NP phrase = ph.getPhrase(token.tokenId, book, dicts);
							//book.animateEntities.put(token.tokenId, phrase);
							System.out.println("5b " + quote.sentenceId + " " + quote.attributionId + " i " + i + " prevvId" + prevId);
							break;
						}
					//}				
				i--;
				}
			}
			else
				System.out.println("MAP NULL");
		}
	//*/

/*
					if (token.pos.startsWith("NN") && token.deprel == "nsubj" && token.quotation == false && token.ner == "PERSON"){
						quote.attributionId = i;
						break;
					}
					if (token.pos.startsWith("NN") && token.deprel == "nsubj" && token.quotation == false){
						quote.attributionId = i;
						break;
					}
					if (token.deprel == "nsubj" && token.quotation == false){
						quote.attributionId = i;
						break;
					}
			*/		


		for (Quotation quote : quotations.values()){
			
			if (quote.attributionId != 0){
				continue;
			}

			
		}
		Map<Integer, Integer> attribId = new HashMap<Integer, Integer>();


		for (Quotation quote : quotations.values()) {
			
			if (attribId.get(quote.p) == null){
				if (quote.attributionId != 0)
					attribId.put(quote.p, quote.attributionId);
			}else	
				quote.attributionId = attribId.get(quote.p);

		}
	
		book.quotations = Lists.newArrayList();
		for (Quotation quote : quotations.values()) {
			book.quotations.add(quote);
		}
		
	}

}
