# index.py — Streamlit version of your flashcards app
# Run locally:  streamlit run index.py
# Deploy on Streamlit Cloud with requirements: streamlit

import os
import json
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Flashcard App", page_icon="🃏", layout="centered")


def load_flashcards():
    """
    Load flashcards from data.json.
    Accepts either {"flashcards":[...]} or a raw list [... ].
    """
    here = os.path.dirname(__file__)
    candidates = [
        os.path.join(here, "data.json"),
        os.path.join(here, "..", "data.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "flashcards" in data and isinstance(data["flashcards"], list):
                return data["flashcards"]
            if isinstance(data, list):
                return data
    return []


cards = load_flashcards()

# Inject your exact HTML+CSS+JS, but feed data from Python into JS.
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flashcard App</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #f3f4f6;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 1rem;
    }}
    .flashcard-container {{
      width: 100%;
      max-width: 640px;
      background-color: #ffffff;
      border-radius: 1.5rem;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      padding: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      min-height: 500px;
    }}
    .card-content {{
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 1rem;
      width: 100%;
    }}
    .card-content p {{
      font-size: 1.5rem;
      line-height: 1.75rem;
      font-weight: 500;
      color: #374151;
      margin-bottom: 1rem;
    }}
    .phrasal-verb {{
      background-color: #dbeafe;
      color: #1e40af;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .phrasal-verb-en {{
      background-color: #d1fae5;
      color: #065f46;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      position: relative;
      cursor: help;
    }}
    .phrasal-verb-en:hover::after {{
      content: attr(data-translation);
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%);
      background-color: #1f2937;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      white-space: nowrap;
      z-index: 1000;
      font-size: 0.875rem;
      margin-bottom: 4px;
    }}
    .logical-connective {{
      background-color: #fef3c7;
      color: #92400e;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .advanced-vocab {{
      background-color: #e9d5ff;
      color: #6b21a8;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      position: relative;
      cursor: help;
    }}
    .advanced-vocab:hover::after {{
      content: attr(data-translation);
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%);
      background-color: #1f2937;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      white-space: nowrap;
      z-index: 1000;
      font-size: 0.875rem;
      margin-bottom: 4px;
    }}
    .ielts-question {{
      font-size: 1.5rem;
      font-weight: 600;
      color: #1e40af;
      margin-bottom: 1.5rem;
      cursor: pointer;
      padding: 1rem;
      border: 2px dashed #3b82f6;
      border-radius: 0.5rem;
      transition: all 0.3s;
    }}
    .ielts-question:hover {{
      background-color: #eff6ff;
      border-color: #2563eb;
    }}
    .ielts-answer {{
      font-size: 1.125rem;
      line-height: 1.75rem;
      color: #374151;
      text-align: left;
      padding: 1rem;
    }}
  </style>
</head>
<body>
  <div class="flashcard-container">
    <h1 class="text-3xl font-bold text-gray-800 mb-4">Speaking Flashcards for Eiki</h1>
    <hr class="w-full h-1 bg-gray-200 rounded my-4">

    <div class="flex flex-col sm:flex-row justify-center gap-4 mb-6 w-full">
      <div class="flex items-center space-x-2">
        <input type="radio" id="sentences" name="card_type" value="sentence" class="form-radio text-blue-600 h-4 w-4" checked>
        <label for="sentences" class="text-lg font-medium text-gray-700">Sentences</label>
      </div>
      <div class="flex items-center space-x-2">
        <input type="radio" id="vocabulary" name="card_type" value="vocabulary" class="form-radio text-blue-600 h-4 w-4">
        <label for="vocabulary" class="text-lg font-medium text-gray-700">Vocabulary</label>
      </div>
      <div class="flex items-center space-x-2">
        <input type="radio" id="phrasal_verbs" name="card_type" value="phrasal_verbs" class="form-radio text-blue-600 h-4 w-4">
        <label for="phrasal_verbs" class="text-lg font-medium text-gray-700">Phrasal Verbs</label>
      </div>
      <div class="flex items-center space-x-2">
        <input type="radio" id="ielts_questions" name="card_type" value="ielts_questions" class="form-radio text-blue-600 h-4 w-4">
        <label for="ielts_questions" class="text-lg font-medium text-gray-700">IELTS Questions</label>
      </div>
    </div>

    <div class="text-gray-500 mb-4" id="card-counter"></div>

    <div class="card-content border border-gray-300 rounded-xl p-6 w-full flex flex-col justify-center items-center">
      <div id="verb-group" class="text-lg font-bold text-green-600 mb-3 text-center"></div>
      <div id="ielts-question" class="ielts-question w-full" style="display: none;"></div>
      <div id="chinese-text" class="text-2xl sm:text-3xl font-semibold text-gray-800 mb-4 text-center"></div>
      <div id="english-text" class="text-xl sm:text-2xl text-gray-600 transition-opacity duration-300 ease-in-out opacity-0 mt-4 text-center"></div>
      <div id="ielts-answer" class="ielts-answer w-full" style="display: none;"></div>
    </div>

    <div class="flex flex-wrap justify-center gap-4 mt-8 w-full">
      <button id="show-hide-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
        Show/Hide English
      </button>
      <button id="next-btn" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
        Next Card
      </button>
      <button id="shuffle-btn" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50">
        Shuffle Cards
      </button>
    </div>
  </div>

  <script>
    // Data injected from Streamlit
    const flashcardData = {json.dumps(cards, ensure_ascii=False)};

    let filteredData = [];
    let cardIndex = 0;
    let showTranslation = false;

    const chineseText = document.getElementById('chinese-text');
    const englishText = document.getElementById('english-text');
    const cardCounter = document.getElementById('card-counter');
    const verbGroupDisplay = document.getElementById('verb-group');
    const ieltsQuestion = document.getElementById('ielts-question');
    const ieltsAnswer = document.getElementById('ielts-answer');
    const showHideBtn = document.getElementById('show-hide-btn');
    const nextBtn = document.getElementById('next-btn');
    const shuffleBtn = document.getElementById('shuffle-btn');
    const cardTypeRadios = document.getElementsByName('card_type');

    function shuffleArray(array) {{
      for (let i = array.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }}
    }}

    function filterAndShuffleCards() {{
      const selectedType = document.querySelector('input[name="card_type"]:checked')?.value || 'sentence';
      filteredData = (flashcardData || []).filter(card => card.type === selectedType);
      shuffleArray(filteredData);
      cardIndex = 0;
      showTranslation = false;
    }}

    function highlightPhrasalVerbs(text, phrasalVerbs, isChinese) {{
      if (!phrasalVerbs || !Array.isArray(phrasalVerbs) || phrasalVerbs.length === 0) {{
        return text;
      }}
      let highlighted = text;
      const className = isChinese ? 'phrasal-verb' : 'phrasal-verb-en';
      
      // Sort by length (longest first) to avoid partial matches
      const sorted = [...phrasalVerbs].sort((a, b) => {{
        const aText = isChinese ? a.chinese : a.english;
        const bText = isChinese ? b.chinese : b.english;
        return bText.length - aText.length;
      }});

      sorted.forEach(pv => {{
        const pvText = isChinese ? pv.chinese : pv.english;
        
        if (isChinese) {{
          // For Chinese, use exact match (no tense variations)
          const escaped = pvText.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const regex = new RegExp(escaped, 'gi');
          highlighted = highlighted.replace(regex, (match) => {{
            return `<span class="${{className}}">${{match}}</span>`;
          }});
        }} else {{
          // For English, handle tense variations including irregular verbs
          // Split phrasal verb into verb and particle(s)
          const parts = pvText.trim().split(/\\s+/);
          if (parts.length >= 2) {{
            const baseVerb = parts[0].toLowerCase();
            const particle = parts.slice(1).join(' ');
            
            // Irregular verb forms mapping
            const irregularVerbs = {{
              'take': ['take', 'takes', 'took', 'taken', 'taking'],
              'get': ['get', 'gets', 'got', 'gotten', 'getting'],
              'go': ['go', 'goes', 'went', 'gone', 'going'],
              'come': ['come', 'comes', 'came', 'coming'],
              'make': ['make', 'makes', 'made', 'making'],
              'break': ['break', 'breaks', 'broke', 'broken', 'breaking'],
              'bring': ['bring', 'brings', 'brought', 'bringing'],
              'run': ['run', 'runs', 'ran', 'running'],
              'give': ['give', 'gives', 'gave', 'given', 'giving'],
              'set': ['set', 'sets', 'setting'],
              'cut': ['cut', 'cuts', 'cutting'],
              'fall': ['fall', 'falls', 'fell', 'fallen', 'falling'],
              'hang': ['hang', 'hangs', 'hung', 'hanging'],
              'hold': ['hold', 'holds', 'held', 'holding'],
              'keep': ['keep', 'keeps', 'kept', 'keeping'],
              'leave': ['leave', 'leaves', 'left', 'leaving'],
              'pull': ['pull', 'pulls', 'pulled', 'pulling'],
              'back': ['back', 'backs', 'backed', 'backing'],
              'look': ['look', 'looks', 'looked', 'looking'],
              'turn': ['turn', 'turns', 'turned', 'turning'],
              'call': ['call', 'calls', 'called', 'calling'],
              'carry': ['carry', 'carries', 'carried', 'carrying'],
              'cool': ['cool', 'cools', 'cooled', 'cooling'],
              'cover': ['cover', 'covers', 'covered', 'covering'],
              'crack': ['crack', 'cracks', 'cracked', 'cracking'],
              'cross': ['cross', 'crosses', 'crossed', 'crossing'],
              'die': ['die', 'dies', 'died', 'dying'],
              'dig': ['dig', 'digs', 'dug', 'digging'],
              'do': ['do', 'does', 'did', 'done', 'doing'],
              'drag': ['drag', 'drags', 'dragged', 'dragging'],
              'draw': ['draw', 'draws', 'drew', 'drawn', 'drawing'],
              'dress': ['dress', 'dresses', 'dressed', 'dressing'],
              'drift': ['drift', 'drifts', 'drifted', 'drifting'],
              'drive': ['drive', 'drives', 'drove', 'driven', 'driving'],
              'drop': ['drop', 'drops', 'dropped', 'dropping'],
              'dry': ['dry', 'dries', 'dried', 'drying'],
              'eat': ['eat', 'eats', 'ate', 'eaten', 'eating'],
              'ease': ['ease', 'eases', 'eased', 'easing'],
              'end': ['end', 'ends', 'ended', 'ending'],
              'face': ['face', 'faces', 'faced', 'facing'],
              'factor': ['factor', 'factors', 'factored', 'factoring'],
              'fade': ['fade', 'fades', 'faded', 'fading'],
              'fasten': ['fasten', 'fastens', 'fastened', 'fastening'],
              'fight': ['fight', 'fights', 'fought', 'fighting'],
              'figure': ['figure', 'figures', 'figured', 'figuring'],
              'fill': ['fill', 'fills', 'filled', 'filling'],
              'filter': ['filter', 'filters', 'filtered', 'filtering'],
              'find': ['find', 'finds', 'found', 'finding'],
              'finish': ['finish', 'finishes', 'finished', 'finishing'],
              'fire': ['fire', 'fires', 'fired', 'firing'],
              'fix': ['fix', 'fixes', 'fixed', 'fixing'],
              'fit': ['fit', 'fits', 'fitted', 'fitting'],
              'grow': ['grow', 'grows', 'grew', 'grown', 'growing'],
              'hand': ['hand', 'hands', 'handed', 'handing'],
              'knock': ['knock', 'knocks', 'knocked', 'knocking'],
              'let': ['let', 'lets', 'let', 'letting'],
              'move': ['move', 'moves', 'moved', 'moving'],
              'pass': ['pass', 'passes', 'passed', 'passing'],
              'pay': ['pay', 'pays', 'paid', 'paying'],
              'pick': ['pick', 'picks', 'picked', 'picking'],
              'point': ['point', 'points', 'pointed', 'pointing'],
              'sit': ['sit', 'sits', 'sat', 'sitting'],
              'stand': ['stand', 'stands', 'stood', 'standing'],
              'talk': ['talk', 'talks', 'talked', 'talking'],
              'think': ['think', 'thinks', 'thought', 'thinking'],
              'throw': ['throw', 'throws', 'threw', 'thrown', 'throwing'],
              'work': ['work', 'works', 'worked', 'working']
            }};
            
            const escapedParticle = particle.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            
            // Check if this is an irregular verb
            let verbForms = [];
            if (irregularVerbs[baseVerb]) {{
              verbForms = irregularVerbs[baseVerb];
            }} else {{
              // Regular verb: generate forms
              verbForms = [
                baseVerb,
                baseVerb + 's',
                baseVerb + 'ed',
                baseVerb + 'ing',
                baseVerb + 'es'
              ];
            }}
            
            // Create pattern matching any of the verb forms followed by particle
            const verbPattern = verbForms.map(v => v.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')).join('|');
            const pattern = `\\\\b(${{verbPattern}})\\\\s+${{escapedParticle}}\\\\b`;
            const regex = new RegExp(pattern, 'gi');
            
            highlighted = highlighted.replace(regex, (match) => {{
              return `<span class="${{className}}">${{match}}</span>`;
            }});
          }} else {{
            // Single word phrasal verb (less common, use exact match with tense variations)
            const baseWord = pvText.toLowerCase();
            const pattern = `\\\\b${{baseWord}}[a-z]*\\\\b`;
            const regex = new RegExp(pattern, 'gi');
            highlighted = highlighted.replace(regex, (match) => {{
              if (match.toLowerCase().startsWith(baseWord)) {{
                return `<span class="${{className}}">${{match}}</span>`;
              }}
              return match;
            }});
          }}
        }}
      }});

      return highlighted;
    }}

    // Phrasal verb to Chinese translation mapping
    const phrasalVerbTranslations = {{
      "focus on": "专注于",
      "raise awareness": "提高意识",
      "passed down": "传承",
      "gather around": "聚集在",
      "bring closer": "拉近",
      "give out": "发放",
      "change to": "改变为",
      "developed fully": "完全发展",
      "establish connections": "建立联系",
      "grow up": "成长",
      "learn from": "从...学习",
      "wind down": "放松",
      "fall asleep": "入睡",
      "slip into": "进入",
      "pick up": "学习",
      "bumped into": "撞到",
      "accompany to": "陪同到",
      "get bumped": "被撞",
      "looked up": "查找",
      "brought to": "带到",
      "put in": "投入",
      "paid off": "得到回报",
      "follow one's heart": "跟随内心",
      "speak for": "代表",
      "have an impact on": "对...有影响",
      "align with": "与...一致",
      "familiar with": "熟悉",
      "equipped with": "配备",
      "dedicate to": "致力于",
      "prepared for": "为...准备",
      "get close to": "接近",
      "get into": "进入",
      "get to know": "了解",
      "connect with": "与...联系",
      "depends on": "取决于",
      "feel proud of": "为...感到骄傲",
      "go anywhere": "去任何地方",
      "inclined towards": "倾向于",
      "make an impact": "产生影响",
      "driven by": "由...驱动",
      "puts focus on": "关注",
      "plays a role": "发挥作用",
      "suits me": "适合我",
      "updating wardrobe": "更新衣柜",
      "boost tourism": "促进旅游业",
      "stimulate demands": "刺激需求",
      "try on": "试穿",
      "cover the needs": "满足需求",
      "pay for": "支付",
      "redeem for": "兑换",
      "pay by": "通过...支付",
      "make sure": "确保",
      "build awareness": "建立意识",
      "follow rules": "遵守规则",
      "full of": "充满",
      "enrich experiences": "丰富经历",
      "go for": "追求",
      "release stress": "释放压力",
      "let out": "释放",
      "serve purposes": "服务于目的",
      "unlock opportunities": "解锁机会",
      "helps with": "有助于",
      "spike interest": "激发兴趣",
      "master skills": "掌握技能",
      "fade away": "淡出",
      "get off work": "下班",
      "come from": "来自",
      "based on": "基于",
      "rush into": "匆忙进入",
      "take time": "花时间",
      "find chances": "找到机会",
      "practice speaking": "练习口语",
      "travel abroad": "出国旅行",
      "get lost": "迷路",
      "ask for": "询问",
      "involved in": "参与"
    }};

    function formatIELTSAnswer(text) {{
      // Add line breaks before points, reasons, and conclusions
      let formatted = text;
      
      // Patterns to match (case insensitive) - order matters!
      // Match conclusions first (they usually come at the end)
      formatted = formatted.replace(/(\\s|^)(In conclusion,|To conclude,|To sum up,|In short,|In summary,)/gi, '<br><br>$2');
      
      // Match numbered points and reasons
      formatted = formatted.replace(/(\\s|^)(Point 1:|Point 2:|Point 3:|Point 4:|Point 5:)/gi, '<br><br>$2');
      formatted = formatted.replace(/(\\s|^)(Reason 1:|Reason 2:|Reason 3:|Reason 4:)/gi, '<br><br>$2');
      
      // Match ordinal points (First, Second, Third, etc.)
      formatted = formatted.replace(/(\\s|^)(First,|Second,|Third,|Fourth,|Fifth,|Finally,)/gi, '<br><br>$2');
      
      // Match transition phrases that start new points
      formatted = formatted.replace(/(\\s|^)(As for|Moreover,|Furthermore,|Additionally,|Also,)/gi, '<br><br>$2');
      
      return formatted;
    }}

    function highlightIELTSAnswer(text, logicalConnectives, phrasalVerbs, advancedVocab) {{
      let highlighted = text;
      
      // Format with line breaks first
      highlighted = formatIELTSAnswer(highlighted);
      
      // Highlight logical connectives
      if (logicalConnectives && logicalConnectives.length > 0) {{
        logicalConnectives.forEach(conn => {{
          const escaped = conn.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
          highlighted = highlighted.replace(regex, (match) => {{
            return `<span class="logical-connective">${{match}}</span>`;
          }});
        }});
      }}
      
      // Highlight phrasal verbs with Chinese translation
      if (phrasalVerbs && phrasalVerbs.length > 0) {{
        phrasalVerbs.forEach(pv => {{
          const translation = phrasalVerbTranslations[pv.toLowerCase()] || '';
          const parts = pv.trim().split(/\\s+/);
          if (parts.length >= 2) {{
            const baseVerb = parts[0].toLowerCase();
            const particle = parts.slice(1).join(' ');
            const escapedParticle = particle.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            const pattern = `\\\\b${{baseVerb}}[a-z]*\\\\s+${{escapedParticle}}\\\\b`;
            const regex = new RegExp(pattern, 'gi');
            highlighted = highlighted.replace(regex, (match) => {{
              return `<span class="phrasal-verb-en" data-translation="${{translation}}">${{match}}</span>`;
            }});
          }} else {{
            // Single word phrasal verb
            const escaped = pv.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
            highlighted = highlighted.replace(regex, (match) => {{
              return `<span class="phrasal-verb-en" data-translation="${{translation}}">${{match}}</span>`;
            }});
          }}
        }});
      }}
      
      // Highlight advanced vocabulary with Chinese translation
      if (advancedVocab && Array.isArray(advancedVocab)) {{
        advancedVocab.forEach(vocab => {{
          const word = vocab.word || vocab;
          const translation = vocab.translation || '';
          const escaped = word.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
          highlighted = highlighted.replace(regex, (match) => {{
            return `<span class="advanced-vocab" data-translation="${{translation}}">${{match}}</span>`;
          }});
        }});
      }}
      
      return highlighted;
    }}

    function renderCard() {{
      if (filteredData.length === 0) {{
        chineseText.innerHTML = "No cards available.";
        englishText.innerHTML = "";
        englishText.classList.add('opacity-0');
        verbGroupDisplay.innerText = "";
        ieltsQuestion.style.display = 'none';
        ieltsAnswer.style.display = 'none';
        cardCounter.innerText = "0/0";
        return;
      }}
      const currentCard = filteredData[cardIndex];
      const selectedType = document.querySelector('input[name="card_type"]:checked')?.value || 'sentence';
      
      // Handle IELTS questions
      if (selectedType === 'ielts_questions') {{
        verbGroupDisplay.style.display = 'none';
        chineseText.style.display = 'none';
        englishText.style.display = 'none';
        ieltsQuestion.style.display = 'block';
        ieltsQuestion.innerText = currentCard.question || "";
        ieltsAnswer.style.display = showTranslation ? 'block' : 'none';
        
        if (showTranslation && currentCard.answer) {{
          let highlightedAnswer = currentCard.answer;
          if (currentCard.logicalConnectives || currentCard.phrasalVerbs || currentCard.advancedVocab) {{
            highlightedAnswer = highlightIELTSAnswer(
              currentCard.answer,
              currentCard.logicalConnectives,
              currentCard.phrasalVerbs,
              currentCard.advancedVocab
            );
          }}
          ieltsAnswer.innerHTML = highlightedAnswer;
        }}
        cardCounter.innerText = `${{cardIndex + 1}}/${{filteredData.length}}`;
        return;
      }}
      
      // Regular cards (sentences, vocabulary, phrasal verbs)
      ieltsQuestion.style.display = 'none';
      ieltsAnswer.style.display = 'none';
      chineseText.style.display = 'block';
      englishText.style.display = 'block';
      
      // Display verb group for phrasal verbs
      if (selectedType === 'phrasal_verbs' && currentCard.verbGroup) {{
        verbGroupDisplay.innerText = `Verb: ${{currentCard.verbGroup.toUpperCase()}}`;
        verbGroupDisplay.style.display = 'block';
      }} else {{
        verbGroupDisplay.style.display = 'none';
      }}
      
      if (selectedType === 'phrasal_verbs' && currentCard.phrasalVerbs) {{
        // Highlight phrasal verbs - always set innerHTML for both
        const highlightedChinese = highlightPhrasalVerbs(currentCard.chinese || "", currentCard.phrasalVerbs, true);
        const highlightedEnglish = highlightPhrasalVerbs(currentCard.english || "", currentCard.phrasalVerbs, false);
        chineseText.innerHTML = highlightedChinese;
        // Always set the innerHTML, then control visibility with opacity
        englishText.innerHTML = highlightedEnglish;
      }} else {{
        // Regular rendering for sentences and vocabulary
        chineseText.innerText = currentCard.chinese || "";
        englishText.innerText = currentCard.english || "";
      }}
      
      // Control visibility after setting content
      if (showTranslation) {{
        englishText.classList.remove('opacity-0');
      }} else {{
        englishText.classList.add('opacity-0');
      }}
      cardCounter.innerText = `${{cardIndex + 1}}/${{filteredData.length}}`;
    }}

    function handleShowHide() {{ showTranslation = !showTranslation; renderCard(); }}
    function handleNextCard() {{ cardIndex = (cardIndex + 1) % filteredData.length; showTranslation = false; renderCard(); }}
    function handleShuffle() {{ filterAndShuffleCards(); renderCard(); }}

    // Click handler for IELTS questions
    ieltsQuestion.addEventListener('click', () => {{
      const selectedType = document.querySelector('input[name="card_type"]:checked')?.value || 'sentence';
      if (selectedType === 'ielts_questions') {{
        showTranslation = !showTranslation;
        renderCard();
      }}
    }});

    showHideBtn.addEventListener('click', handleShowHide);
    nextBtn.addEventListener('click', handleNextCard);
    shuffleBtn.addEventListener('click', handleShuffle);

    cardTypeRadios.forEach(radio => {{
      radio.addEventListener('change', () => {{
        filterAndShuffleCards();
        renderCard();
      }});
    }});

    // Initial setup
    window.onload = () => {{
      filterAndShuffleCards();
      renderCard();
    }};

    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{ e.preventDefault(); handleShowHide(); }}
      if (e.code === 'ArrowRight') {{ e.preventDefault(); handleNextCard(); }}
    }});
  </script>
</body>
</html>"""

# Render the full HTML app inside Streamlit
# Increase height if needed
html(html_content, height=900, scrolling=True)
