package novels.annotators;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.Iterator;

import novels.Token;
import novels.Book;

import org.maltparser.MaltParserService;
import org.maltparser.core.exception.MaltChainedException;
import org.maltparser.core.symbol.SymbolTable;
import org.maltparser.core.syntaxgraph.DependencyStructure;
import org.maltparser.core.syntaxgraph.edge.Edge;
import org.maltparser.core.syntaxgraph.node.DependencyNode;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphEdge;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.BasicDependenciesAnnotation;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.trees.GrammaticalRelation;

public class SyntaxAnnotator {

	public static String MALT_DIR = "files/malt/";
	public static String MALT = "engmalt.linear-1.7.mco";
	public int id = 0;

	public static String getAgent(Book book, int index) {
		Token token = book.tokens.get(index);
		if (token.head != -1) {
			Token head = book.tokens.get(token.head);
			// collapse conj (e.g. "He and Darcy went ..." where syntax = darcy
			// ->/conj He, he ->/nsubj went)
			if (token.deprel.equals("conj") && head.head != -1) {
				token = head;
				head = book.tokens.get(head.head);
			}

			if (head.pos.startsWith("V")
					&& (token.deprel.equals("nsubj") || token.deprel
							.equals("agent"))) {
				TreeSet<Integer> deps = book.dependents.get(head.tokenId);

				/*
				 * for (int d : deps) { Token dep = book.tokens.get(d); if
				 * (dep.deprel.equals("dobj")) { String term=dep.lemma; if
				 * (book.tokenToCharacter.containsKey(dep.tokenId)) { term="[" +
				 * book
				 * .characters[book.tokenToCharacter.get(dep.tokenId).getCharacterId
				 * ()].name + "]"; } return head.lemma + "_" + term; } }
				 */
				return head.word;
			}
			if (head.pos.equals("MD")
					&& (token.deprel.equals("nsubj") || token.deprel
							.equals("agent"))) {
				boolean modal = false;
				TreeSet<Integer> deps = book.dependents.get(head.tokenId);

				String deplemma = null;
				for (int d : deps) {
					Token dep = book.tokens.get(d);
					if (dep.pos.startsWith("V")) {
						modal = true;
						deplemma = dep.word;
					}
				}
				if (modal) {
					return deplemma;
				}
			}
		}
		return null;
	}

	public static String getPatient(Book book, int index) {
		Token token = book.tokens.get(index);
		if (token.head != -1) {
			Token head = book.tokens.get(token.head);
			// collapse conj (e.g. "He and Darcy went ..." where syntax = darcy
			// ->/conj He, he ->/nsubj went)
			if (token.deprel.equals("conj") && head.head != -1) {
				token = head;
				head = book.tokens.get(head.head);
			}
			if (head.pos.startsWith("V")
					&& (token.deprel.equals("dobj") || token.deprel
							.equals("nsubjpass"))) {
				return head.word;
			}
		}
		return null;
	}
	
	public static void setCharacterIds(Book book)
	{
		try{
			for (Token anno : book.tokens) {
					if (book.tokenToCharacter.containsKey(anno.tokenId)) {
						anno.characterId=book.tokenToCharacter.get(anno.tokenId).getCharacterId();
					}
				}
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static String getMods(Book book, int index) {
		Token token = book.tokens.get(index);
		if (token.head != -1) {
			Token head = book.tokens.get(token.head);
			// collapse conj (e.g. "He and Darcy went ..." where syntax = darcy
			// ->/conj He, he ->/nsubj went)
			if (token.deprel.equals("conj") && head.head != -1) {
				token = head;
				head = book.tokens.get(head.head);
			}
			if ((head.pos.startsWith("NN") || head.pos.startsWith("JJ"))
					&& token.deprel.equals("nsubj")) {
				TreeSet<Integer> deps = book.dependents.get(head.tokenId);
				boolean predicate = false;
				for (int d : deps) {
					Token dep = book.tokens.get(d);
					if (dep.lemma.equals("be")) {
						predicate = true;
					}
				}
				if (predicate) {
					return head.word;
				}
			}
		}
		return null;
	}

	public static String getPoss(Book book, int index) {
		Token token = book.tokens.get(index);
		if (token.head != -1) {
			Token head = book.tokens.get(token.head);
			// collapse conj (e.g. "He and Darcy went ..." where syntax = darcy
			// ->/conj He, he ->/nsubj went)
			if (token.deprel.equals("conj") && head.head != -1) {
				token = head;
				head = book.tokens.get(head.head);
			}
			if (token.deprel.equals("poss")) {
				return head.word;
			}
		}
		return null;
	}

	public static ArrayList<Token> readDocs(List<String> infiles) {
		ArrayList<Token> tokens = new ArrayList<Token>();
		int parOffset = 0;
		int sentenceOffset = 0;
		int tokenOffset = 0;
		try {

			for (String infile : infiles) {
				BufferedReader in1 = new BufferedReader(new InputStreamReader(
						new FileInputStream(infile), "UTF-8"));
				String str1;

				while ((str1 = in1.readLine()) != null) {
					Token token = new Token(str1.trim(), parOffset,
							sentenceOffset, tokenOffset);
					tokens.add(token);
				}
				Token lastToken = tokens.get(tokens.size() - 1);
				parOffset = lastToken.p + 1;
				sentenceOffset = lastToken.sentenceID + 1;
				tokenOffset = lastToken.tokenId + 1;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return tokens;
	}

	public static ArrayList<Token> readDoc(String infile) {
		ArrayList<Token> tokens = new ArrayList<Token>();
		try {
			BufferedReader in1 = new BufferedReader(new InputStreamReader(
					new FileInputStream(infile), "UTF-8"));
			String str1;

			while ((str1 = in1.readLine()) != null) {
				Token token = new Token(str1.trim());
				tokens.add(token);

			}

			in1.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
		return tokens;
	}

	// This is largely unneeded, https://universaldependencies.org/docs/en/overview/migration-guidelines.html
	// "onsidering the new treatment of prepositional phrases the basic representation already has direct dependencies
	// between content words which makes the collapsed representation largely obsolete. On the other hand, the propagation of
	// conjunt dependencies still adds useful dependencies in UD.""
	public static HashSet<Integer> getRecursiveDeps(int index, Book book) {
		// Modified by: Sky
		HashSet<Integer> deps = new HashSet<Integer>();
		TreeSet<Integer> deps_treeset = book.dependents.get(index);
		for (int i : deps_treeset) {
			deps.add(i);
		}
		return deps;
		// HashSet<Integer> deps = new HashSet<Integer>();
		// if (book.dependents.containsKey(index)) {
		// 	TreeSet<Integer> nextDeps = book.dependents.get(index);
		// 	for (int i : nextDeps) {
		// 			deps.addAll(getRecursiveDeps(i, book));			
		// 	}
		// }
		// deps.add(index);
		// return deps;
	}

	public static void setDependents(Book book) {
		book.dependents = new HashMap<Integer, TreeSet<Integer>>();
		for (Token tok : book.tokens) {
			int head = tok.head;
			if (head != -1) {
				TreeSet<Integer> deps = null;
				if (book.dependents.containsKey(head)) {
					deps = book.dependents.get(head);
				} else {
					deps = new TreeSet<Integer>();
				}
				deps.add(tok.tokenId);
				book.dependents.put(head, deps);

			}
		}
	}

	MaltParserService service;
	StanfordCoreNLP pipeline;
	int count;
	boolean stateLess;

	public void initialize() {
		try {

			if (!stateLess) {
				System.out.println("Setting Properties...");
				Properties props = new Properties();
				props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, depparse");
				//props.setProperty("ssplit.boundaryMultiTokenRegex", "/\'\'/, /``/");
				//props.setProperty("ssplit.boundaryMultiTokenRegex", "/``//\'\'/");
				props.setProperty("ssplit.boundaryMultiTokenRegex", "/\'\'|``/");
				pipeline = new StanfordCoreNLP(props);
				System.out.println("Properties set.");

				service = new MaltParserService(id);

				System.out.println("Creating maltparser with id " + id);
				service.initializeParserModel(String.format(
						"-c %s -m parse -w %s -lfi parser.log", MALT, MALT_DIR));
			}
		} catch (MaltChainedException e) {
			e.printStackTrace();
		}
	}

	public ArrayList<Token> process(String doc) throws Exception {

		// ADDED BY SKY:
		Properties props_no_ssplit = new Properties();
		props_no_ssplit.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, depparse");
		props_no_ssplit.setProperty("ssplit.isOneSentence", "true");
		StanfordCoreNLP pipeline_no_ssplit = new StanfordCoreNLP(props_no_ssplit);
		// ***

		/*
		 * First see if newlines separate paragraphs or if they show up in the
		 * middle of lines.
		 */
		String[] sents = doc.split("\n");
		float punctCount = 0;
		float nonPuntCount = 0;
		boolean newlineParagraphs = false;
		for (String sent : sents) {
			if (sent.length() > 0) {
				String last = sent.substring(sent.length() - 1);
				if (last.equals(".") || last.equals("\"") || last.equals(":")
						|| last.equals("?") || last.equals("!")) {
					punctCount++;
				} else {
					nonPuntCount++;
				}
			}
		}

		if (punctCount / (punctCount + nonPuntCount) > .5) {
			newlineParagraphs = true;
		}

		if (service == null || count % 10 == 0) {
			initialize();
		}
		count++;

		ArrayList<Token> allWords = new ArrayList<Token>();

		Annotation document = new Annotation(doc);

		System.err.println("Tagging and parsing...");
		pipeline.annotate(document);

		int s = 0;
		int t = 0;
		int p = 0;
		
		System.out.println("Tokenizing Sentences...");
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		
		int totalSentences = sentences.size() - 1;
		System.out.println("Sentences tokenized.");

		ArrayList<ArrayList<Token>> sentenceannos = new ArrayList<ArrayList<Token>>();
		
		for (int cm_indx = 0; cm_indx < sentences.size(); cm_indx++) {
			CoreMap sentence = sentences.get(cm_indx);

			if (s % 100 == 0 || s == totalSentences) {
				double ratio = ((double) s) / totalSentences;
				System.err.print(String.format(
						"\t%.3f (%s out of %s) processed\r", ratio, s,
						totalSentences));
			}

			ArrayList<Token> annos = new ArrayList<Token>();
			
			for (CoreLabel token : sentence.get(TokensAnnotation.class)) {

				String word = token.get(TextAnnotation.class);
				String pos = token.get(PartOfSpeechAnnotation.class);
				String lemma = token.get(LemmaAnnotation.class);
				String ne = token.get(NamedEntityTagAnnotation.class);
				int beginOffset = token.beginPosition();
				int endOffset = token.endPosition();
				String whitespaceAfter = token.after();
				String original = token.originalText();

				Token anno = new Token();
				anno.original = original;
				anno.word = word;
				anno.pos = pos;
				anno.lemma = lemma;
				anno.ner = ne;
				anno.sentenceID = s;
				anno.tokenId = t;
				anno.beginOffset = beginOffset;
				anno.endOffset = endOffset;
				anno.quotation = "O";
				anno.setWhitespaceAfter(whitespaceAfter);
				anno.p = p;
				annos.add(anno);
				allWords.add(anno);
				t++;
				whitespaceAfter = anno.whitespaceAfter;

				if (token.after().matches("\\n{2,}")
						|| (token.after().matches("\\n") && newlineParagraphs)) {
					p++;
				}
			}

			sentenceannos.add(annos);
		}

		// fix sentence mistakes (like: "Yes!" he said).
		ArrayList<ArrayList<Token>> new_sentences = new ArrayList<ArrayList<Token>>();
		// Added by: Sky
		ArrayList<CoreMap> sentences_fixed = new ArrayList<CoreMap>();

		boolean lastFlag = false;

		for (int s_idx = 0; s_idx < sentenceannos.size(); s_idx++) {

			boolean lowercaseFlag = false;

			ArrayList<Token> annos = sentenceannos.get(s_idx);
			if (annos.size() > 0
					&& annos.get(0).word.toLowerCase()
							.equals(annos.get(0).word)
					&& annos.get(0).word.matches(".*[a-z].*")) {
				lowercaseFlag = true;
			}

			// I think what this is doing is just combining sentences together, if an error was detected.
			if (lastFlag == true && lowercaseFlag == true) {
				// Error detected, initialize this_annos as previous sentence (it's not done)
				ArrayList<Token> this_annos = new_sentences.get(new_sentences
						.size() - 1);
				// Join current sentence with previous sentence.
				for (int t_idx = 0; t_idx < annos.size(); t_idx++) {
					Token anno = annos.get(t_idx);
					this_annos.add(anno);
				}
				new_sentences.set(new_sentences.size() - 1, this_annos);
				// ***
				String sentence_fixed = sentences_fixed.get(sentences_fixed.size()-1).toString();
				sentence_fixed = sentence_fixed + " " + sentences.get(s_idx).toString();
				Annotation sent_annotate = new Annotation(sentence_fixed);
				pipeline_no_ssplit.annotate(sent_annotate);
				CoreMap sentence_fixed_coremap = sent_annotate.get(SentencesAnnotation.class).get(0);

				// System.out.println(sent_annotate.get(SentencesAnnotation.class));

				sentences_fixed.set(sentences_fixed.size()-1, sentence_fixed_coremap);

			} else {
				// No error detected.
				ArrayList<Token> newannos = new ArrayList<Token>();
				// Just put the current sentence into newannos.
				for (int t_idx = 0; t_idx < annos.size(); t_idx++) {
					Token anno = annos.get(t_idx);
					newannos.add(anno);
				}
				new_sentences.add(newannos);
				// ***
				sentences_fixed.add(sentences.get(s_idx));
			}

			lastFlag=false;
			if (annos.size() > 1) {
				Token ultimate = annos.get(annos.size() - 1);
				Token penultimate = annos.get(annos.size() - 2);
				if (ultimate.word.equals("''")
						&& (penultimate.word.equals("?") || penultimate.word
								.equals("!"))) {
					lastFlag = true;
				}
			}
		}

		// System.out.println("new_sentences:" + new_sentences.size() + ", sentences: " + sentences_fixed.size());

		for (int s_idx = 0; s_idx < new_sentences.size(); s_idx++) {
			
			ArrayList<Token> annos = new_sentences.get(s_idx);
			CoreMap sentence = sentences_fixed.get(s_idx);

			int oldId, newId;
			int id = 1;
			oldId = id;
			String[] parseTokens = new String[annos.size()];
			for (Token anno : annos) {
				String parseToken = String.format("%d\t%s\t%s\t%s\t%s\t%s", id,
						anno.word, anno.lemma, anno.pos, anno.pos, "_");
				parseTokens[id - 1] = parseToken;
				id++;
				anno.sentenceID = s;
			}
			s++; // 
			newId = id;		
///*
			SemanticGraph dependencies = sentence.get(BasicDependenciesAnnotation.class);
			
			//String dep_type = "CollapsedDependenciesAnnotation";
			//System.out.println(dep_type+" ===>>");
			//if (s == 2321){
			//if (s >= 2622 && s < 2626){			
			//System.out.println("\n\n\nSentence " + s + ": ---------------\n"+sentence.toString() +"\n");
			//System.out.println("DEPENDENCIES: "+dependencies.toList());
			//System.out.println("DEPENDENCIES SIZE: "+dependencies.size() + " " + newId + " " + oldId + " " + (newId - oldId));
			//}			
			List<SemanticGraphEdge> edge_set1 = dependencies.edgeListSorted();
			int j=0;
			Iterator it = dependencies.getRoots().iterator();
			IndexedWord root = (IndexedWord) it.next();			
			int index = dependencies.size() + 1;
			
			Token rAnno = annos.get(root.index() -1);
			rAnno.head = -1;
			rAnno.deprel = "null";
			//if (s >= 2622 && s < 2626)
			//System.out.println((j-1) + ": (" + root.index() + " -1) " +  + rAnno.tokenId + " " + rAnno.head + " " + rAnno.deprel + " " + rAnno.word + " ");
			//annos.set(root.index()-1, rAnno);
			
			for(SemanticGraphEdge edge : edge_set1){
				j++;
				//System.out.println("------EDGE DEPENDENCY: "+j);
			    
				IndexedWord dep = edge.getDependent();
				String dependent = dep.word();
				int dependent_index = dep.index();
				Token anno = annos.get(dependent_index - 1);

				int diff = dependent_index - index;
				if (diff == 2){
					diff--;
				}
				
				IndexedWord gov = edge.getGovernor();
				String governor = gov.word();
				int governor_index = gov.index();
				GrammaticalRelation relation = edge.getRelation();
				
				if (diff == 0 || gov.index() - dep.index() == 0){	
		//			System.out.println("\n\t\tHere\n");
					continue;					
				}				
				
				//System.out.println("No:"+j+" "+relation.toString()
				//	+" "+ (dep.index()) +" : "+dep.word()+"->: "+ (gov.index()) +" " + gov.word() + " " + diff);
				
				index = dep.index();
				anno.head =   anno.tokenId + (gov.index() - dep.index()); 
				anno.deprel = relation.toString();
				annos.set(dependent_index -1, anno);
																																																																																																																																										
				//System.out.println(j + ": (" + dep.index() + " " + gov.index() + ") " + anno.tokenId + " " + anno.head + " " + anno.deprel +" " +  anno.word + " " + diff);
			}
//*/			
			//System.out.println("-----------------");

					

		}
		p++;

		System.err.println();

		//service.terminateParserModel();

		return allWords;

	}

	public static String getPath(int s, int t, ArrayList<Token> allWords) {
		
		//System.out.println("get path " + s + " " + t);
		boolean collapseConj = true;

		Token source = allWords.get(s);
		Token target = allWords.get(t);
		int sourceHead = s;
		Token parent = null;

		boolean withinSentenceMatch = false;
		int withinSentenceCommon = -1;
		ArrayList<Integer> up = new ArrayList<Integer>();
		ArrayList<String> ups = new ArrayList<String>();
		while (sourceHead != -1) {
			parent = allWords.get(sourceHead);
			sourceHead = parent.head;
			up.add(parent.tokenId);
			ups.add(parent.deprel);
		}

		sourceHead = t;
		parent = null;

		ArrayList<Integer> down = new ArrayList<Integer>();
		ArrayList<String> downs = new ArrayList<String>();

		while (sourceHead != -1) {
			parent = allWords.get(sourceHead);
			sourceHead = parent.head;
			down.add(parent.tokenId);
			downs.add(parent.deprel);

			if (up.contains(sourceHead) && sourceHead != -1) {
				withinSentenceMatch = true;
				withinSentenceCommon = sourceHead;
				break;
			}

		}

		String chain = "";
		if (withinSentenceMatch) {
			for (int i = 0; i < up.size(); i++) {
				int index = up.get(i);
				String deprel = ups.get(i);
				chain += "^" + deprel;
				if (index == withinSentenceCommon) {
					break;
				}
			}

			for (int i = down.size() - 1; i >= 0; i--) {
				String deprel = downs.get(i);
				chain += ">" + deprel;
			}
		} else {
			for (int i = 0; i < up.size(); i++) {
				String deprel = ups.get(i);
				chain += "^" + deprel;
			}

			int jump = target.sentenceID - source.sentenceID;
			for (int i = 0; i < jump; i++) {
				chain += "=root";
			}

			for (int i = down.size() - 1; i >= 0; i--) {
				String deprel = downs.get(i);
				chain += ">" + deprel;
			}
		}

		if (collapseConj) {
			chain = chain.replaceAll("^conj", "");
			chain = chain.replaceAll(">conj", "");
		}
		return chain;
	}

	public static int getEndpoint(int i, Book book) {
		Token token = book.tokens.get(i);
		int corefHead = -1;
		int head = token.coref;

		if (token.coref != 0) {
			corefHead = token.coref;
			int hops = 0;
			if (corefHead != 0) {
				head = corefHead;
			}
			while (corefHead != 0) {
				hops++;
				if (hops > 100) {
					break;
				}
				Token tokenHead = book.tokens.get(corefHead);

				if (tokenHead.coref == corefHead) {
					break;
				}
				corefHead = tokenHead.coref;
				if (corefHead != 0) {
					head = corefHead;
				}
			}
				
		}
		return head;
	}

}
