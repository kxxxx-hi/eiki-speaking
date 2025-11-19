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
    }}
    .phrasal-verb-translation {{
      color: #065f46;
      font-size: 0.9em;
      margin-left: 4px;
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
    }}
    .advanced-vocab-translation {{
      color: #6b21a8;
      font-size: 0.9em;
      margin-left: 4px;
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
    .ielts-synonyms {{
      font-size: 1rem;
      line-height: 1.6rem;
      color: #374151;
      text-align: left;
      padding: 1rem;
      margin-top: 1rem;
      border-top: 2px solid #e5e7eb;
    }}
    .synonyms-title {{
      font-size: 1.25rem;
      font-weight: 600;
      color: #1e40af;
      margin-bottom: 0.75rem;
    }}
    .synonym-item {{
      margin-bottom: 0.5rem;
      padding-left: 1rem;
    }}
    .synonym-word {{
      font-weight: 600;
      color: #6b21a8;
    }}
    .synonym-translation {{
      color: #6b21a8;
      font-size: 0.9em;
      margin-left: 4px;
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
      <div id="ielts-synonyms" class="ielts-synonyms w-full" style="display: none;"></div>
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
    const ieltsSynonyms = document.getElementById('ielts-synonyms');
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
      
      // Helper function to avoid matching inside HTML tags
      function replaceNotInTags(text, pattern, replacement) {{
        // Split by HTML tags, process text parts only
        const parts = text.split(/(<[^>]+>)/);
        for (let i = 0; i < parts.length; i += 2) {{
          // Only process text parts (even indices)
          if (parts[i]) {{
            parts[i] = parts[i].replace(pattern, replacement);
          }}
        }}
        return parts.join('');
      }}
      
      // Highlight logical connectives
      if (logicalConnectives && logicalConnectives.length > 0) {{
        logicalConnectives.forEach(conn => {{
          const escaped = conn.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
          highlighted = replaceNotInTags(highlighted, regex, (match) => {{
            return `<span class="logical-connective">${{match}}</span>`;
          }});
        }});
      }}
      
      // Highlight phrasal verbs with Chinese translation (sort by length, longest first)
      if (phrasalVerbs && phrasalVerbs.length > 0) {{
        const sortedPhrasalVerbs = [...phrasalVerbs].sort((a, b) => b.length - a.length);
        sortedPhrasalVerbs.forEach(pv => {{
          const translation = phrasalVerbTranslations[pv.toLowerCase()] || '';
          const parts = pv.trim().split(/\\s+/);
          if (parts.length >= 2) {{
            const baseVerb = parts[0].toLowerCase();
            const particle = parts.slice(1).join(' ');
            const escapedParticle = particle.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            const pattern = new RegExp(`\\\\b${{baseVerb}}[a-z]*\\\\s+${{escapedParticle}}\\\\b`, 'gi');
            highlighted = replaceNotInTags(highlighted, pattern, (match) => {{
              if (translation) {{
                return `<span class="phrasal-verb-en">${{match}}</span><span class="phrasal-verb-translation"> ${{translation}}</span>`;
              }}
              return `<span class="phrasal-verb-en">${{match}}</span>`;
            }});
          }} else {{
            // Single word phrasal verb
            const escaped = pv.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
            highlighted = replaceNotInTags(highlighted, regex, (match) => {{
              if (translation) {{
                return `<span class="phrasal-verb-en">${{match}}</span><span class="phrasal-verb-translation"> ${{translation}}</span>`;
              }}
              return `<span class="phrasal-verb-en">${{match}}</span>`;
            }});
          }}
        }});
      }}
      
      // Highlight advanced vocabulary with Chinese translation (sort by length, longest first)
      if (advancedVocab && Array.isArray(advancedVocab)) {{
        const sortedVocab = [...advancedVocab].sort((a, b) => {{
          const aWord = (a.word || a).toLowerCase();
          const bWord = (b.word || b).toLowerCase();
          return bWord.length - aWord.length;
        }});
        
        sortedVocab.forEach(vocab => {{
          const word = vocab.word || vocab;
          const translation = vocab.translation || '';
          const escaped = word.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
          const regex = new RegExp(`\\\\b${{escaped}}\\\\b`, 'gi');
          highlighted = replaceNotInTags(highlighted, regex, (match) => {{
            if (translation) {{
              return `<span class="advanced-vocab">${{match}}</span><span class="advanced-vocab-translation"> ${{translation}}</span>`;
            }}
            return `<span class="advanced-vocab">${{match}}</span>`;
          }});
        }});
      }}
      
      return highlighted;
    }}

    // Advanced vocabulary to simpler synonyms mapping
    const advancedVocabSynonyms = {{
      "heritage": [
        {{"word": "tradition", "translation": "传统"}},
        {{"word": "culture", "translation": "文化"}},
        {{"word": "custom", "translation": "习俗"}}
      ],
      "belonging": [
        {{"word": "feeling part of", "translation": "归属感"}},
        {{"word": "connection", "translation": "联系"}},
        {{"word": "being included", "translation": "被包含"}}
      ],
      "strengthens": [
        {{"word": "makes stronger", "translation": "使更强"}},
        {{"word": "improves", "translation": "改善"}},
        {{"word": "builds", "translation": "建立"}}
      ],
      "mature": [
        {{"word": "fully developed", "translation": "完全发展"}},
        {{"word": "ready", "translation": "准备好"}},
        {{"word": "complete", "translation": "完整的"}}
      ],
      "infrastructure": [
        {{"word": "basic facilities", "translation": "基础设施"}},
        {{"word": "public buildings", "translation": "公共建筑"}},
        {{"word": "services", "translation": "服务"}}
      ],
      "established": [
        {{"word": "built", "translation": "建立"}},
        {{"word": "set up", "translation": "设置"}},
        {{"word": "created", "translation": "创建"}}
      ],
      "residential": [
        {{"word": "living areas", "translation": "居住区"}},
        {{"word": "neighborhoods", "translation": "社区"}},
        {{"word": "housing areas", "translation": "住房区"}}
      ],
      "awareness": [
        {{"word": "knowledge", "translation": "知识"}},
        {{"word": "understanding", "translation": "理解"}},
        {{"word": "knowing about", "translation": "了解"}}
      ],
      "therapy": [
        {{"word": "treatment", "translation": "治疗"}},
        {{"word": "help", "translation": "帮助"}},
        {{"word": "counseling", "translation": "咨询"}}
      ],
      "consultation": [
        {{"word": "advice", "translation": "建议"}},
        {{"word": "help", "translation": "帮助"}},
        {{"word": "discussion", "translation": "讨论"}}
      ],
      "meaningful": [
        {{"word": "important", "translation": "重要的"}},
        {{"word": "valuable", "translation": "有价值的"}},
        {{"word": "significant", "translation": "有意义的"}}
      ],
      "precious": [
        {{"word": "valuable", "translation": "珍贵的"}},
        {{"word": "important", "translation": "重要的"}},
        {{"word": "special", "translation": "特殊的"}}
      ],
      "thoughtful": [
        {{"word": "considerate", "translation": "体贴的"}},
        {{"word": "caring", "translation": "关心的"}},
        {{"word": "kind", "translation": "善良的"}}
      ],
      "considerate": [
        {{"word": "thoughtful", "translation": "体贴的"}},
        {{"word": "caring", "translation": "关心的"}},
        {{"word": "kind", "translation": "善良的"}}
      ],
      "mentality": [
        {{"word": "way of thinking", "translation": "思维方式"}},
        {{"word": "attitude", "translation": "态度"}},
        {{"word": "mindset", "translation": "心态"}}
      ],
      "cognitive": [
        {{"word": "thinking", "translation": "思维"}},
        {{"word": "mental", "translation": "心理的"}},
        {{"word": "brain", "translation": "大脑"}}
      ],
      "predict": [
        {{"word": "tell in advance", "translation": "提前告知"}},
        {{"word": "guess", "translation": "猜测"}},
        {{"word": "forecast", "translation": "预测"}}
      ],
      "requires": [
        {{"word": "needs", "translation": "需要"}},
        {{"word": "must have", "translation": "必须有"}},
        {{"word": "demands", "translation": "要求"}}
      ],
      "wholesome": [
        {{"word": "healthy", "translation": "健康的"}},
        {{"word": "good", "translation": "好的"}},
        {{"word": "positive", "translation": "积极的"}}
      ],
      "literacy": [
        {{"word": "reading and writing", "translation": "读写能力"}},
        {{"word": "language skills", "translation": "语言技能"}},
        {{"word": "education", "translation": "教育"}}
      ],
      "humble": [
        {{"word": "modest", "translation": "谦逊的"}},
        {{"word": "not proud", "translation": "不骄傲"}},
        {{"word": "polite", "translation": "礼貌的"}}
      ],
      "educated": [
        {{"word": "well-learned", "translation": "受过良好教育的"}},
        {{"word": "knowledgeable", "translation": "有知识的"}},
        {{"word": "learned", "translation": "有学问的"}}
      ],
      "genuinely": [
        {{"word": "really", "translation": "真正地"}},
        {{"word": "truly", "translation": "真实地"}},
        {{"word": "sincerely", "translation": "真诚地"}}
      ],
      "advocates": [
        {{"word": "supports", "translation": "支持"}},
        {{"word": "promotes", "translation": "促进"}},
        {{"word": "encourages", "translation": "鼓励"}}
      ],
      "apologetic": [
        {{"word": "sorry", "translation": "抱歉的"}},
        {{"word": "regretful", "translation": "后悔的"}},
        {{"word": "remorseful", "translation": "悔恨的"}}
      ],
      "tutorials": [
        {{"word": "lessons", "translation": "课程"}},
        {{"word": "guides", "translation": "指南"}},
        {{"word": "instructions", "translation": "说明"}}
      ],
      "guided": [
        {{"word": "led", "translation": "引导"}},
        {{"word": "showed", "translation": "展示"}},
        {{"word": "helped", "translation": "帮助"}}
      ],
      "successfully": [
        {{"word": "well", "translation": "成功地"}},
        {{"word": "with success", "translation": "成功"}},
        {{"word": "effectively", "translation": "有效地"}}
      ],
      "definitely": [
        {{"word": "certainly", "translation": "肯定地"}},
        {{"word": "surely", "translation": "确定地"}},
        {{"word": "for sure", "translation": "肯定"}}
      ],
      "impact": [
        {{"word": "effect", "translation": "影响"}},
        {{"word": "influence", "translation": "影响"}},
        {{"word": "change", "translation": "改变"}}
      ],
      "align": [
        {{"word": "match", "translation": "匹配"}},
        {{"word": "fit with", "translation": "适合"}},
        {{"word": "agree with", "translation": "同意"}}
      ],
      "agile": [
        {{"word": "quick", "translation": "快速的"}},
        {{"word": "fast", "translation": "快的"}},
        {{"word": "flexible", "translation": "灵活的"}}
      ],
      "efficiency": [
        {{"word": "productivity", "translation": "生产力"}},
        {{"word": "effectiveness", "translation": "有效性"}},
        {{"word": "speed", "translation": "速度"}}
      ],
      "commitments": [
        {{"word": "responsibilities", "translation": "责任"}},
        {{"word": "duties", "translation": "职责"}},
        {{"word": "obligations", "translation": "义务"}}
      ],
      "exhibit": [
        {{"word": "show", "translation": "展示"}},
        {{"word": "display", "translation": "显示"}},
        {{"word": "present", "translation": "呈现"}}
      ],
      "precious": [
        {{"word": "valuable", "translation": "珍贵的"}},
        {{"word": "important", "translation": "重要的"}},
        {{"word": "treasured", "translation": "珍贵的"}}
      ],
      "fossils": [
        {{"word": "ancient remains", "translation": "古代遗骸"}},
        {{"word": "old bones", "translation": "古骨"}},
        {{"word": "prehistoric remains", "translation": "史前遗骸"}}
      ],
      "ancient": [
        {{"word": "very old", "translation": "非常古老的"}},
        {{"word": "old", "translation": "古老的"}},
        {{"word": "from long ago", "translation": "很久以前的"}}
      ],
      "profound": [
        {{"word": "deep", "translation": "深刻的"}},
        {{"word": "strong", "translation": "强烈的"}},
        {{"word": "meaningful", "translation": "有意义的"}}
      ],
      "roots": [
        {{"word": "origins", "translation": "起源"}},
        {{"word": "beginnings", "translation": "开始"}},
        {{"word": "foundation", "translation": "基础"}}
      ],
      "perspective": [
        {{"word": "viewpoint", "translation": "观点"}},
        {{"word": "opinion", "translation": "意见"}},
        {{"word": "way of seeing", "translation": "看法"}}
      ],
      "driven": [
        {{"word": "led by", "translation": "由...领导"}},
        {{"word": "caused by", "translation": "由...引起"}},
        {{"word": "powered by", "translation": "由...驱动"}}
      ],
      "significantly": [
        {{"word": "greatly", "translation": "大大地"}},
        {{"word": "a lot", "translation": "很多"}},
        {{"word": "much", "translation": "非常"}}
      ],
      "observations": [
        {{"word": "things I noticed", "translation": "我注意到的事情"}},
        {{"word": "what I see", "translation": "我看到的东西"}},
        {{"word": "findings", "translation": "发现"}}
      ],
      "frequency": [
        {{"word": "how often", "translation": "频率"}},
        {{"word": "rate", "translation": "比率"}},
        {{"word": "regularity", "translation": "规律性"}}
      ],
      "wardrobe": [
        {{"word": "clothes collection", "translation": "衣服收藏"}},
        {{"word": "clothing", "translation": "服装"}},
        {{"word": "outfits", "translation": "服装"}}
      ],
      "opportunities": [
        {{"word": "chances", "translation": "机会"}},
        {{"word": "possibilities", "translation": "可能性"}},
        {{"word": "options", "translation": "选择"}}
      ],
      "catering": [
        {{"word": "food services", "translation": "餐饮服务"}},
        {{"word": "food", "translation": "食物"}},
        {{"word": "meals", "translation": "餐食"}}
      ],
      "stimulate": [
        {{"word": "encourage", "translation": "鼓励"}},
        {{"word": "boost", "translation": "促进"}},
        {{"word": "increase", "translation": "增加"}}
      ],
      "merchandise": [
        {{"word": "products", "translation": "产品"}},
        {{"word": "goods", "translation": "商品"}},
        {{"word": "items", "translation": "物品"}}
      ],
      "aesthetical": [
        {{"word": "artistic", "translation": "艺术的"}},
        {{"word": "beautiful", "translation": "美丽的"}},
        {{"word": "tasteful", "translation": "有品味的"}}
      ],
      "diverse": [
        {{"word": "various", "translation": "多样的"}},
        {{"word": "different", "translation": "不同的"}},
        {{"word": "many kinds", "translation": "多种"}}
      ],
      "range": [
        {{"word": "variety", "translation": "种类"}},
        {{"word": "selection", "translation": "选择"}},
        {{"word": "collection", "translation": "收藏"}}
      ],
      "classy": [
        {{"word": "elegant", "translation": "优雅的"}},
        {{"word": "stylish", "translation": "时尚的"}},
        {{"word": "fancy", "translation": "精美的"}}
      ],
      "pleasant": [
        {{"word": "nice", "translation": "好的"}},
        {{"word": "enjoyable", "translation": "愉快的"}},
        {{"word": "comfortable", "translation": "舒适的"}}
      ],
      "convenience": [
        {{"word": "ease", "translation": "便利"}},
        {{"word": "comfort", "translation": "舒适"}},
        {{"word": "easy access", "translation": "容易获得"}}
      ],
      "redeem": [
        {{"word": "exchange", "translation": "兑换"}},
        {{"word": "trade", "translation": "交易"}},
        {{"word": "swap", "translation": "交换"}}
      ],
      "essentials": [
        {{"word": "basic needs", "translation": "基本需求"}},
        {{"word": "necessities", "translation": "必需品"}},
        {{"word": "basics", "translation": "基础"}}
      ],
      "installment": [
        {{"word": "monthly payment", "translation": "月付"}},
        {{"word": "payment plan", "translation": "付款计划"}},
        {{"word": "paying in parts", "translation": "分期付款"}}
      ],
      "crypto": [
        {{"word": "digital money", "translation": "数字货币"}},
        {{"word": "online currency", "translation": "在线货币"}},
        {{"word": "virtual money", "translation": "虚拟货币"}}
      ],
      "convenient": [
        {{"word": "easy", "translation": "方便的"}},
        {{"word": "handy", "translation": "便利的"}},
        {{"word": "simple", "translation": "简单的"}}
      ],
      "fundamentals": [
        {{"word": "basics", "translation": "基础"}},
        {{"word": "essentials", "translation": "必需品"}},
        {{"word": "foundation", "translation": "基础"}}
      ],
      "competitions": [
        {{"word": "contests", "translation": "竞赛"}},
        {{"word": "games", "translation": "比赛"}},
        {{"word": "events", "translation": "活动"}}
      ],
      "athletes": [
        {{"word": "sports players", "translation": "运动员"}},
        {{"word": "players", "translation": "选手"}},
        {{"word": "competitors", "translation": "竞争者"}}
      ],
      "fairness": [
        {{"word": "being fair", "translation": "公平"}},
        {{"word": "justice", "translation": "正义"}},
        {{"word": "equal treatment", "translation": "平等对待"}}
      ],
      "discipline": [
        {{"word": "self-control", "translation": "自律"}},
        {{"word": "order", "translation": "秩序"}},
        {{"word": "rules", "translation": "规则"}}
      ],
      "role models": [
        {{"word": "examples", "translation": "榜样"}},
        {{"word": "people to follow", "translation": "值得学习的人"}},
        {{"word": "heroes", "translation": "英雄"}}
      ],
      "organized": [
        {{"word": "well-planned", "translation": "有组织的"}},
        {{"word": "orderly", "translation": "有序的"}},
        {{"word": "structured", "translation": "结构化的"}}
      ],
      "civilized": [
        {{"word": "polite", "translation": "文明的"}},
        {{"word": "well-behaved", "translation": "行为良好的"}},
        {{"word": "cultured", "translation": "有文化的"}}
      ],
      "thrilling": [
        {{"word": "exciting", "translation": "刺激的"}},
        {{"word": "adventurous", "translation": "冒险的"}},
        {{"word": "exciting", "translation": "令人兴奋的"}}
      ],
      "adrenaline": [
        {{"word": "excitement", "translation": "兴奋"}},
        {{"word": "energy", "translation": "能量"}},
        {{"word": "thrill", "translation": "刺激"}}
      ],
      "rush": [
        {{"word": "surge", "translation": "激增"}},
        {{"word": "burst", "translation": "爆发"}},
        {{"word": "wave", "translation": "浪潮"}}
      ],
      "release": [
        {{"word": "let out", "translation": "释放"}},
        {{"word": "free", "translation": "释放"}},
        {{"word": "get rid of", "translation": "摆脱"}}
      ],
      "affordable": [
        {{"word": "cheap", "translation": "负担得起的"}},
        {{"word": "inexpensive", "translation": "便宜的"}},
        {{"word": "low-cost", "translation": "低成本的"}}
      ],
      "barrier-free": [
        {{"word": "easy to access", "translation": "无障碍的"}},
        {{"word": "open to all", "translation": "向所有人开放"}},
        {{"word": "accessible", "translation": "可获得的"}}
      ],
      "accessible": [
        {{"word": "easy to reach", "translation": "容易到达的"}},
        {{"word": "available", "translation": "可获得的"}},
        {{"word": "reachable", "translation": "可到达的"}}
      ],
      "critical": [
        {{"word": "important", "translation": "批判的"}},
        {{"word": "key", "translation": "关键的"}},
        {{"word": "essential", "translation": "必要的"}}
      ],
      "enriching": [
        {{"word": "fulfilling", "translation": "充实的"}},
        {{"word": "rewarding", "translation": "有回报的"}},
        {{"word": "satisfying", "translation": "令人满意的"}}
      ],
      "fulfilling": [
        {{"word": "satisfying", "translation": "充实的"}},
        {{"word": "rewarding", "translation": "有回报的"}},
        {{"word": "meaningful", "translation": "有意义的"}}
      ],
      "practical": [
        {{"word": "useful", "translation": "实用的"}},
        {{"word": "real", "translation": "实际的"}},
        {{"word": "helpful", "translation": "有帮助的"}}
      ],
      "survival": [
        {{"word": "staying alive", "translation": "生存"}},
        {{"word": "living", "translation": "生活"}},
        {{"word": "existence", "translation": "存在"}}
      ],
      "essential": [
        {{"word": "necessary", "translation": "必要的"}},
        {{"word": "important", "translation": "重要的"}},
        {{"word": "needed", "translation": "需要的"}}
      ],
      "advanced": [
        {{"word": "higher level", "translation": "高级的"}},
        {{"word": "complex", "translation": "复杂的"}},
        {{"word": "sophisticated", "translation": "复杂的"}}
      ],
      "unlock": [
        {{"word": "open up", "translation": "解锁"}},
        {{"word": "access", "translation": "访问"}},
        {{"word": "get", "translation": "获得"}}
      ],
      "complicated": [
        {{"word": "complex", "translation": "复杂的"}},
        {{"word": "difficult", "translation": "困难的"}},
        {{"word": "hard", "translation": "难的"}}
      ],
      "prospects": [
        {{"word": "chances", "translation": "前景"}},
        {{"word": "opportunities", "translation": "机会"}},
        {{"word": "possibilities", "translation": "可能性"}}
      ],
      "master": [
        {{"word": "learn well", "translation": "掌握"}},
        {{"word": "be good at", "translation": "擅长"}},
        {{"word": "excel at", "translation": "精通"}}
      ],
      "favored": [
        {{"word": "preferred", "translation": "偏爱的"}},
        {{"word": "liked", "translation": "喜欢的"}},
        {{"word": "chosen", "translation": "选择的"}}
      ],
      "interest-driven": [
        {{"word": "based on benefits", "translation": "利益驱动的"}},
        {{"word": "for gain", "translation": "为了利益"}},
        {{"word": "profit-based", "translation": "基于利润的"}}
      ],
      "genuine": [
        {{"word": "real", "translation": "真诚的"}},
        {{"word": "true", "translation": "真实的"}},
        {{"word": "sincere", "translation": "真诚的"}}
      ],
      "personality": [
        {{"word": "character", "translation": "个性"}},
        {{"word": "nature", "translation": "本性"}},
        {{"word": "traits", "translation": "特征"}}
      ],
      "risk-averse": [
        {{"word": "careful", "translation": "风险规避的"}},
        {{"word": "cautious", "translation": "谨慎的"}},
        {{"word": "avoiding risks", "translation": "避免风险"}}
      ],
      "memorize": [
        {{"word": "remember", "translation": "记忆"}},
        {{"word": "learn by heart", "translation": "背诵"}},
        {{"word": "commit to memory", "translation": "记住"}}
      ],
      "opportunities": [
        {{"word": "chances", "translation": "机会"}},
        {{"word": "possibilities", "translation": "可能性"}},
        {{"word": "options", "translation": "选择"}}
      ],
      "confusing": [
        {{"word": "unclear", "translation": "令人困惑的"}},
        {{"word": "hard to understand", "translation": "难以理解"}},
        {{"word": "puzzling", "translation": "令人困惑的"}}
      ],
      "challenging": [
        {{"word": "difficult", "translation": "有挑战的"}},
        {{"word": "hard", "translation": "困难的"}},
        {{"word": "tough", "translation": "艰难的"}}
      ],
      "beneficial": [
        {{"word": "helpful", "translation": "有益的"}},
        {{"word": "good for", "translation": "对...好"}},
        {{"word": "useful", "translation": "有用的"}}
      ],
      "communications": [
        {{"word": "talking", "translation": "沟通"}},
        {{"word": "conversations", "translation": "对话"}},
        {{"word": "exchanges", "translation": "交流"}}
      ],
      "international": [
        {{"word": "global", "translation": "国际的"}},
        {{"word": "worldwide", "translation": "全球的"}},
        {{"word": "between countries", "translation": "国家间的"}}
      ],
      "multinational": [
        {{"word": "across countries", "translation": "跨国的"}},
        {{"word": "global", "translation": "全球的"}},
        {{"word": "worldwide", "translation": "世界范围的"}}
      ],
      "primarily": [
        {{"word": "mainly", "translation": "主要地"}},
        {{"word": "mostly", "translation": "大部分"}},
        {{"word": "chiefly", "translation": "主要地"}}
      ],
      "fundamental": [
        {{"word": "basic", "translation": "基本的"}},
        {{"word": "essential", "translation": "必要的"}},
        {{"word": "important", "translation": "重要的"}}
      ],
      "atmosphere": [
        {{"word": "environment", "translation": "氛围"}},
        {{"word": "mood", "translation": "气氛"}},
        {{"word": "feeling", "translation": "感觉"}}
      ],
      "concentrate": [
        {{"word": "focus", "translation": "集中注意力"}},
        {{"word": "pay attention", "translation": "注意"}},
        {{"word": "think hard", "translation": "认真思考"}}
      ],
      "immerse": [
        {{"word": "involve deeply", "translation": "沉浸"}},
        {{"word": "get into", "translation": "进入"}},
        {{"word": "focus completely", "translation": "完全专注"}}
      ],
      "academics": [
        {{"word": "school subjects", "translation": "学术"}},
        {{"word": "studies", "translation": "学习"}},
        {{"word": "education", "translation": "教育"}}
      ],
      "talent": [
        {{"word": "natural ability", "translation": "天赋"}},
        {{"word": "gift", "translation": "天赋"}},
        {{"word": "skill", "translation": "技能"}}
      ],
      "potential": [
        {{"word": "possibility", "translation": "潜力"}},
        {{"word": "ability", "translation": "能力"}},
        {{"word": "what could be", "translation": "可能"}}
      ],
      "employment": [
        {{"word": "jobs", "translation": "就业"}},
        {{"word": "work", "translation": "工作"}},
        {{"word": "career", "translation": "职业"}}
      ],
      "well-rounded": [
        {{"word": "complete", "translation": "全面的"}},
        {{"word": "balanced", "translation": "平衡的"}},
        {{"word": "all-around", "translation": "全面的"}}
      ],
      "professional": [
        {{"word": "work-related", "translation": "职业的"}},
        {{"word": "business-like", "translation": "专业的"}},
        {{"word": "formal", "translation": "正式的"}}
      ],
      "interest-driven": [
        {{"word": "based on benefits", "translation": "利益驱动的"}},
        {{"word": "for gain", "translation": "为了利益"}},
        {{"word": "profit-based", "translation": "基于利润的"}}
      ],
      "various": [
        {{"word": "different", "translation": "各种各样的"}},
        {{"word": "many kinds", "translation": "多种"}},
        {{"word": "diverse", "translation": "多样的"}}
      ],
      "genuine": [
        {{"word": "real", "translation": "真诚的"}},
        {{"word": "true", "translation": "真实的"}},
        {{"word": "sincere", "translation": "真诚的"}}
      ],
      "ulterior": [
        {{"word": "hidden", "translation": "隐藏的"}},
        {{"word": "secret", "translation": "秘密的"}},
        {{"word": "not obvious", "translation": "不明显的"}}
      ],
      "deserve": [
        {{"word": "should get", "translation": "值得"}},
        {{"word": "merit", "translation": "应得"}},
        {{"word": "worthy of", "translation": "值得的"}}
      ],
      "undivided": [
        {{"word": "full", "translation": "专一的"}},
        {{"word": "complete", "translation": "完全的"}},
        {{"word": "total", "translation": "全部的"}}
      ],
      "responsibilities": [
        {{"word": "duties", "translation": "责任"}},
        {{"word": "tasks", "translation": "任务"}},
        {{"word": "jobs", "translation": "工作"}}
      ],
      "productive": [
        {{"word": "efficient", "translation": "高效的"}},
        {{"word": "effective", "translation": "有效的"}},
        {{"word": "useful", "translation": "有用的"}}
      ],
      "candidates": [
        {{"word": "applicants", "translation": "候选人"}},
        {{"word": "people applying", "translation": "申请者"}},
        {{"word": "options", "translation": "选择"}}
      ],
      "definitely": [
        {{"word": "certainly", "translation": "肯定地"}},
        {{"word": "surely", "translation": "确定地"}},
        {{"word": "for sure", "translation": "肯定"}}
      ],
      "solidifies": [
        {{"word": "strengthens", "translation": "巩固"}},
        {{"word": "makes stronger", "translation": "使更强"}},
        {{"word": "builds up", "translation": "建立"}}
      ],
      "incredible": [
        {{"word": "amazing", "translation": "难以置信的"}},
        {{"word": "unbelievable", "translation": "不可思议的"}},
        {{"word": "wonderful", "translation": "极好的"}}
      ],
      "variety": [
        {{"word": "many kinds", "translation": "种类"}},
        {{"word": "selection", "translation": "选择"}},
        {{"word": "range", "translation": "范围"}}
      ],
      "cuisines": [
        {{"word": "types of food", "translation": "菜系"}},
        {{"word": "cooking styles", "translation": "烹饪风格"}},
        {{"word": "food", "translation": "食物"}}
      ],
      "specialties": [
        {{"word": "special dishes", "translation": "特色菜"}},
        {{"word": "famous food", "translation": "名菜"}},
        {{"word": "unique dishes", "translation": "独特菜肴"}}
      ],
      "bustling": [
        {{"word": "busy", "translation": "热闹的"}},
        {{"word": "lively", "translation": "活跃的"}},
        {{"word": "full of activity", "translation": "充满活动的"}}
      ],
      "vibrant": [
        {{"word": "lively", "translation": "充满活力的"}},
        {{"word": "energetic", "translation": "有活力的"}},
        {{"word": "bright", "translation": "明亮的"}}
      ],
      "ambiance": [
        {{"word": "atmosphere", "translation": "氛围"}},
        {{"word": "mood", "translation": "气氛"}},
        {{"word": "feeling", "translation": "感觉"}}
      ],
      "auspicious": [
        {{"word": "lucky", "translation": "吉祥的"}},
        {{"word": "fortunate", "translation": "幸运的"}},
        {{"word": "promising", "translation": "有希望的"}}
      ],
      "glutinous": [
        {{"word": "sticky", "translation": "粘的"}},
        {{"word": "thick", "translation": "厚的"}},
        {{"word": "chewy", "translation": "有嚼劲的"}}
      ],
      "symbolizes": [
        {{"word": "represents", "translation": "象征"}},
        {{"word": "stands for", "translation": "代表"}},
        {{"word": "means", "translation": "意味着"}}
      ],
      "wholeness": [
        {{"word": "completeness", "translation": "完整"}},
        {{"word": "unity", "translation": "统一"}},
        {{"word": "togetherness", "translation": "团结"}}
      ],
      "reunion": [
        {{"word": "getting together", "translation": "团聚"}},
        {{"word": "meeting again", "translation": "重聚"}},
        {{"word": "family gathering", "translation": "家庭聚会"}}
      ],
      "fortune": [
        {{"word": "luck", "translation": "财富"}},
        {{"word": "wealth", "translation": "财富"}},
        {{"word": "success", "translation": "成功"}}
      ],
      "deep-rooted": [
        {{"word": "long-standing", "translation": "根深蒂固的"}},
        {{"word": "traditional", "translation": "传统的"}},
        {{"word": "strongly held", "translation": "根深蒂固的"}}
      ],
      "symbolism": [
        {{"word": "meaning", "translation": "象征意义"}},
        {{"word": "representation", "translation": "代表"}},
        {{"word": "significance", "translation": "意义"}}
      ],
      "irreplaceable": [
        {{"word": "cannot be replaced", "translation": "不可替代的"}},
        {{"word": "unique", "translation": "独特的"}},
        {{"word": "special", "translation": "特殊的"}}
      ],
      "tangible": [
        {{"word": "real", "translation": "具体的"}},
        {{"word": "concrete", "translation": "具体的"}},
        {{"word": "actual", "translation": "实际的"}}
      ],
      "close-knit": [
        {{"word": "tight", "translation": "紧密的"}},
        {{"word": "united", "translation": "团结的"}},
        {{"word": "close", "translation": "亲密的"}}
      ],
      "harmonious": [
        {{"word": "peaceful", "translation": "和谐的"}},
        {{"word": "agreeable", "translation": "和谐的"}},
        {{"word": "balanced", "translation": "平衡的"}}
      ],
      "amplified": [
        {{"word": "increased", "translation": "放大的"}},
        {{"word": "made stronger", "translation": "增强的"}},
        {{"word": "enhanced", "translation": "增强的"}}
      ],
      "ritual": [
        {{"word": "ceremony", "translation": "仪式"}},
        {{"word": "tradition", "translation": "传统"}},
        {{"word": "custom", "translation": "习俗"}}
      ],
      "hassle": [
        {{"word": "trouble", "translation": "麻烦"}},
        {{"word": "bother", "translation": "麻烦"}},
        {{"word": "difficulty", "translation": "困难"}}
      ],
      "approach": [
        {{"word": "way of doing", "translation": "处理"}},
        {{"word": "method", "translation": "方法"}},
        {{"word": "way", "translation": "方式"}}
      ],
      "master chef": [
        {{"word": "expert cook", "translation": "大厨"}},
        {{"word": "professional cook", "translation": "专业厨师"}},
        {{"word": "skilled cook", "translation": "熟练的厨师"}}
      ],
      "conveniences": [
        {{"word": "helpful things", "translation": "便利"}},
        {{"word": "useful services", "translation": "有用的服务"}},
        {{"word": "comforts", "translation": "舒适"}}
      ],
      "lifesavers": [
        {{"word": "very helpful things", "translation": "救命稻草"}},
        {{"word": "solutions", "translation": "解决方案"}},
        {{"word": "help", "translation": "帮助"}}
      ],
      "production": [
        {{"word": "big task", "translation": "复杂的事"}},
        {{"word": "complicated thing", "translation": "复杂的事情"}},
        {{"word": "big effort", "translation": "大努力"}}
      ],
      "vividly": [
        {{"word": "clearly", "translation": "清晰地"}},
        {{"word": "in detail", "translation": "详细地"}},
        {{"word": "brightly", "translation": "明亮地"}}
      ],
      "whimsical": [
        {{"word": "playful", "translation": "异想天开的"}},
        {{"word": "funny", "translation": "有趣的"}},
        {{"word": "imaginative", "translation": "富有想象力的"}}
      ],
      "magically": [
        {{"word": "mysteriously", "translation": "神奇地"}},
        {{"word": "wonderfully", "translation": "奇妙地"}},
        {{"word": "like magic", "translation": "像魔法一样"}}
      ],
      "crave": [
        {{"word": "want badly", "translation": "渴望"}},
        {{"word": "desire", "translation": "渴望"}},
        {{"word": "long for", "translation": "渴望"}}
      ],
      "delightful": [
        {{"word": "pleasant", "translation": "令人愉快的"}},
        {{"word": "enjoyable", "translation": "令人愉快的"}},
        {{"word": "charming", "translation": "迷人的"}}
      ],
      "imaginative": [
        {{"word": "creative", "translation": "富有想象力的"}},
        {{"word": "original", "translation": "原创的"}},
        {{"word": "inventive", "translation": "有创造力的"}}
      ],
      "unavoidable": [
        {{"word": "cannot avoid", "translation": "不可避免的"}},
        {{"word": "certain", "translation": "确定的"}},
        {{"word": "sure to happen", "translation": "肯定会发生"}}
      ],
      "plastered": [
        {{"word": "covered", "translation": "贴满"}},
        {{"word": "filled with", "translation": "充满"}},
        {{"word": "everywhere", "translation": "到处都是"}}
      ],
      "billboards": [
        {{"word": "large signs", "translation": "广告牌"}},
        {{"word": "advertising boards", "translation": "广告板"}},
        {{"word": "posters", "translation": "海报"}}
      ],
      "glossy": [
        {{"word": "shiny", "translation": "光鲜亮丽的"}},
        {{"word": "smooth", "translation": "光滑的"}},
        {{"word": "polished", "translation": "抛光的"}}
      ],
      "cosmetics": [
        {{"word": "makeup", "translation": "化妆品"}},
        {{"word": "beauty products", "translation": "美容产品"}},
        {{"word": "beauty items", "translation": "美容用品"}}
      ],
      "commuters": [
        {{"word": "people who travel to work", "translation": "通勤者"}},
        {{"word": "daily travelers", "translation": "日常通勤者"}},
        {{"word": "workers", "translation": "工作者"}}
      ],
      "profound": [
        {{"word": "deep", "translation": "深刻的"}},
        {{"word": "serious", "translation": "严肃的"}},
        {{"word": "important", "translation": "重要的"}}
      ],
      "dominate": [
        {{"word": "control", "translation": "主导"}},
        {{"word": "lead", "translation": "领导"}},
        {{"word": "rule", "translation": "统治"}}
      ],
      "visually-driven": [
        {{"word": "picture-based", "translation": "视觉驱动的"}},
        {{"word": "image-focused", "translation": "以图像为中心"}},
        {{"word": "visual", "translation": "视觉的"}}
      ],
      "snappy": [
        {{"word": "quick", "translation": "快速的"}},
        {{"word": "fast", "translation": "快的"}},
        {{"word": "brief", "translation": "简短的"}}
      ],
      "eye-catching": [
        {{"word": "attractive", "translation": "吸引眼球的"}},
        {{"word": "noticeable", "translation": "引人注目的"}},
        {{"word": "striking", "translation": "醒目的"}}
      ],
      "shrinking": [
        {{"word": "getting smaller", "translation": "缩小的"}},
        {{"word": "reducing", "translation": "减少的"}},
        {{"word": "decreasing", "translation": "下降的"}}
      ],
      "cautious": [
        {{"word": "careful", "translation": "谨慎的"}},
        {{"word": "watchful", "translation": "警惕的"}},
        {{"word": "alert", "translation": "警觉的"}}
      ],
      "immediate": [
        {{"word": "instant", "translation": "即时的"}},
        {{"word": "right away", "translation": "立即"}},
        {{"word": "quick", "translation": "快速的"}}
      ],
      "wealth": [
        {{"word": "rich information", "translation": "财富"}},
        {{"word": "lots of", "translation": "很多"}},
        {{"word": "abundance", "translation": "丰富"}}
      ],
      "insightful": [
        {{"word": "thoughtful", "translation": "有深度的"}},
        {{"word": "wise", "translation": "明智的"}},
        {{"word": "deep", "translation": "深刻的"}}
      ],
      "downside": [
        {{"word": "disadvantage", "translation": "缺点"}},
        {{"word": "problem", "translation": "问题"}},
        {{"word": "negative side", "translation": "负面"}}
      ],
      "echo chambers": [
        {{"word": "closed groups", "translation": "回音室"}},
        {{"word": "isolated views", "translation": "孤立观点"}},
        {{"word": "same opinions only", "translation": "只有相同意见"}}
      ],
      "cocoons": [
        {{"word": "isolated spaces", "translation": "茧"}},
        {{"word": "closed environments", "translation": "封闭环境"}},
        {{"word": "bubbles", "translation": "气泡"}}
      ],
      "algorithms": [
        {{"word": "computer programs", "translation": "算法"}},
        {{"word": "systems", "translation": "系统"}},
        {{"word": "formulas", "translation": "公式"}}
      ],
      "clickbait": [
        {{"word": "misleading headlines", "translation": "点击诱饵"}},
        {{"word": "trick titles", "translation": "欺骗性标题"}},
        {{"word": "attention-grabbing", "translation": "吸引注意"}}
      ],
      "sensational": [
        {{"word": "shocking", "translation": "耸人听闻的"}},
        {{"word": "exciting", "translation": "令人兴奋的"}},
        {{"word": "dramatic", "translation": "戏剧性的"}}
      ],
      "objective": [
        {{"word": "fair", "translation": "客观的"}},
        {{"word": "unbiased", "translation": "无偏见的"}},
        {{"word": "neutral", "translation": "中立的"}}
      ],
      "vicious cycle": [
        {{"word": "bad circle", "translation": "恶性循环"}},
        {{"word": "endless problem", "translation": "无尽的问题"}},
        {{"word": "repeating trouble", "translation": "重复的麻烦"}}
      ],
      "reinforces": [
        {{"word": "strengthens", "translation": "强化"}},
        {{"word": "makes stronger", "translation": "使更强"}},
        {{"word": "supports", "translation": "支持"}}
      ],
      "biases": [
        {{"word": "prejudices", "translation": "偏见"}},
        {{"word": "unfair views", "translation": "不公平的观点"}},
        {{"word": "favoritism", "translation": "偏袒"}}
      ],
      "fantastic": [
        {{"word": "great", "translation": "极好的"}},
        {{"word": "wonderful", "translation": "极好的"}},
        {{"word": "excellent", "translation": "优秀的"}}
      ],
      "clincher": [
        {{"word": "key point", "translation": "关键因素"}},
        {{"word": "main reason", "translation": "主要原因"}},
        {{"word": "deciding factor", "translation": "决定因素"}}
      ],
      "sheer": [
        {{"word": "pure", "translation": "纯粹的"}},
        {{"word": "simple", "translation": "简单的"}},
        {{"word": "complete", "translation": "完全的"}}
      ],
      "convenience": [
        {{"word": "ease", "translation": "便利"}},
        {{"word": "comfort", "translation": "舒适"}},
        {{"word": "easy access", "translation": "容易获得"}}
      ],
      "accelerates": [
        {{"word": "speeds up", "translation": "加速"}},
        {{"word": "makes faster", "translation": "使更快"}},
        {{"word": "quickens", "translation": "加快"}}
      ],
      "crucial": [
        {{"word": "very important", "translation": "关键的"}},
        {{"word": "essential", "translation": "必要的"}},
        {{"word": "vital", "translation": "至关重要的"}}
      ],
      "logical": [
        {{"word": "reasonable", "translation": "逻辑的"}},
        {{"word": "sensible", "translation": "合理的"}},
        {{"word": "makes sense", "translation": "有道理"}}
      ],
      "strengthens": [
        {{"word": "makes stronger", "translation": "加强"}},
        {{"word": "improves", "translation": "改善"}},
        {{"word": "builds up", "translation": "建立"}}
      ],
      "analyse": [
        {{"word": "examine", "translation": "分析"}},
        {{"word": "study", "translation": "研究"}},
        {{"word": "look at carefully", "translation": "仔细看"}}
      ],
      "essential": [
        {{"word": "necessary", "translation": "必要的"}},
        {{"word": "important", "translation": "重要的"}},
        {{"word": "needed", "translation": "需要的"}}
      ],
      "spark": [
        {{"word": "ignite", "translation": "激发"}},
        {{"word": "create", "translation": "创造"}},
        {{"word": "trigger", "translation": "触发"}}
      ],
      "curiosity": [
        {{"word": "interest", "translation": "好奇心"}},
        {{"word": "wanting to know", "translation": "想知道"}},
        {{"word": "wonder", "translation": "好奇"}}
      ],
      "mathematicians": [
        {{"word": "math experts", "translation": "数学家"}},
        {{"word": "math teachers", "translation": "数学老师"}},
        {{"word": "people who study math", "translation": "研究数学的人"}}
      ],
      "foundation": [
        {{"word": "base", "translation": "基础"}},
        {{"word": "groundwork", "translation": "基础"}},
        {{"word": "starting point", "translation": "起点"}}
      ],
      "significantly": [
        {{"word": "greatly", "translation": "显著地"}},
        {{"word": "a lot", "translation": "很多"}},
        {{"word": "much", "translation": "非常"}}
      ],
      "prospects": [
        {{"word": "chances", "translation": "前景"}},
        {{"word": "opportunities", "translation": "机会"}},
        {{"word": "possibilities", "translation": "可能性"}}
      ],
      "analytical": [
        {{"word": "logical", "translation": "分析的"}},
        {{"word": "thinking", "translation": "思考的"}},
        {{"word": "examining", "translation": "检查的"}}
      ],
      "numerical": [
        {{"word": "number-related", "translation": "数字的"}},
        {{"word": "math", "translation": "数学"}},
        {{"word": "calculating", "translation": "计算的"}}
      ],
      "reliable": [
        {{"word": "trustworthy", "translation": "可靠的"}},
        {{"word": "dependable", "translation": "可靠的"}},
        {{"word": "can be trusted", "translation": "可以信任"}}
      ],
      "well-organised": [
        {{"word": "well-arranged", "translation": "组织良好的"}},
        {{"word": "orderly", "translation": "有序的"}},
        {{"word": "structured", "translation": "结构化的"}}
      ],
      "trustworthy": [
        {{"word": "reliable", "translation": "值得信赖的"}},
        {{"word": "honest", "translation": "诚实的"}},
        {{"word": "can be trusted", "translation": "可以信任"}}
      ],
      "world-famous": [
        {{"word": "known worldwide", "translation": "世界著名的"}},
        {{"word": "internationally known", "translation": "国际知名的"}},
        {{"word": "globally recognized", "translation": "全球认可的"}}
      ],
      "engaging": [
        {{"word": "interesting", "translation": "吸引人的"}},
        {{"word": "captivating", "translation": "吸引人的"}},
        {{"word": "appealing", "translation": "有吸引力的"}}
      ],
      "vivid": [
        {{"word": "clear", "translation": "生动的"}},
        {{"word": "lifelike", "translation": "栩栩如生的"}},
        {{"word": "bright", "translation": "明亮的"}}
      ],
      "bite-sized": [
        {{"word": "short", "translation": "简短的"}},
        {{"word": "quick", "translation": "快速的"}},
        {{"word": "easy to digest", "translation": "容易理解"}}
      ],
      "complicated": [
        {{"word": "complex", "translation": "复杂的"}},
        {{"word": "difficult", "translation": "困难的"}},
        {{"word": "hard", "translation": "难的"}}
      ],
      "mysterious": [
        {{"word": "unknown", "translation": "神秘的"}},
        {{"word": "puzzling", "translation": "令人困惑的"}},
        {{"word": "strange", "translation": "奇怪的"}}
      ],
      "abstract": [
        {{"word": "theoretical", "translation": "抽象的"}},
        {{"word": "not concrete", "translation": "不具体的"}},
        {{"word": "hard to understand", "translation": "难以理解"}}
      ],
      "cutting-edge": [
        {{"word": "latest", "translation": "前沿的"}},
        {{"word": "most advanced", "translation": "最先进的"}},
        {{"word": "newest", "translation": "最新的"}}
      ],
      "dramatically": [
        {{"word": "greatly", "translation": "显著地"}},
        {{"word": "significantly", "translation": "显著地"}},
        {{"word": "a lot", "translation": "很多"}}
      ],
      "state-of-the-art": [
        {{"word": "most advanced", "translation": "最先进的"}},
        {{"word": "latest technology", "translation": "最新技术"}},
        {{"word": "cutting-edge", "translation": "前沿的"}}
      ],
      "transparent": [
        {{"word": "clear", "translation": "透明的"}},
        {{"word": "open", "translation": "开放的"}},
        {{"word": "honest", "translation": "诚实的"}}
      ],
      "approachable": [
        {{"word": "easy to understand", "translation": "平易近人的"}},
        {{"word": "friendly", "translation": "友好的"}},
        {{"word": "accessible", "translation": "可获得的"}}
      ],
      "accessible": [
        {{"word": "easy to reach", "translation": "可获得的"}},
        {{"word": "available", "translation": "可获得的"}},
        {{"word": "reachable", "translation": "可到达的"}}
      ],
      "appreciate": [
        {{"word": "value", "translation": "欣赏"}},
        {{"word": "enjoy", "translation": "享受"}},
        {{"word": "understand", "translation": "理解"}}
      ],
      "core": [
        {{"word": "main", "translation": "核心的"}},
        {{"word": "central", "translation": "中心的"}},
        {{"word": "essential", "translation": "必要的"}}
      ],
      "opportunities": [
        {{"word": "chances", "translation": "机会"}},
        {{"word": "possibilities", "translation": "可能性"}},
        {{"word": "options", "translation": "选择"}}
      ],
      "extracurricular": [
        {{"word": "outside class", "translation": "课外的"}},
        {{"word": "after school", "translation": "放学后"}},
        {{"word": "additional", "translation": "额外的"}}
      ],
      "peers": [
        {{"word": "people same age", "translation": "同龄人"}},
        {{"word": "classmates", "translation": "同学"}},
        {{"word": "equals", "translation": "同等的人"}}
      ],
      "choir": [
        {{"word": "singing group", "translation": "合唱团"}},
        {{"word": "vocal group", "translation": "声乐组"}},
        {{"word": "singers", "translation": "歌手"}}
      ],
      "performing": [
        {{"word": "acting", "translation": "表演"}},
        {{"word": "showing", "translation": "展示"}},
        {{"word": "presenting", "translation": "呈现"}}
      ],
      "bond": [
        {{"word": "connection", "translation": "建立联系"}},
        {{"word": "relationship", "translation": "关系"}},
        {{"word": "link", "translation": "联系"}}
      ],
      "frequently": [
        {{"word": "often", "translation": "经常地"}},
        {{"word": "regularly", "translation": "定期地"}},
        {{"word": "many times", "translation": "多次"}}
      ],
      "recreational": [
        {{"word": "for fun", "translation": "娱乐的"}},
        {{"word": "leisure", "translation": "休闲的"}},
        {{"word": "entertainment", "translation": "娱乐"}}
      ],
      "collaborate": [
        {{"word": "work together", "translation": "合作"}},
        {{"word": "cooperate", "translation": "合作"}},
        {{"word": "team up", "translation": "组队"}}
      ],
      "lasting": [
        {{"word": "long-term", "translation": "持久的"}},
        {{"word": "enduring", "translation": "持久的"}},
        {{"word": "permanent", "translation": "永久的"}}
      ]
    }};

    function generateSynonymsSection(advancedVocab) {{
      if (!advancedVocab || !Array.isArray(advancedVocab) || advancedVocab.length === 0) {{
        return '';
      }}
      
      let html = '<div class="synonyms-title">Synonyms or Paraphrases:</div>';
      
      advancedVocab.forEach(vocab => {{
        const word = vocab.word || vocab;
        const synonyms = advancedVocabSynonyms[word.toLowerCase()];
        
        if (synonyms && synonyms.length > 0) {{
          html += `<div class="synonym-item">`;
          html += `<strong>${{word}}:</strong> `;
          const synonymTexts = synonyms.map(s => 
            `<span class="synonym-word">${{s.word}}</span><span class="synonym-translation"> ${{s.translation}}</span>`
          ).join(', ');
          html += synonymTexts;
          html += `</div>`;
        }}
      }});
      
      return html;
    }}

    function renderCard() {{
      if (filteredData.length === 0) {{
        chineseText.innerHTML = "No cards available.";
        englishText.innerHTML = "";
        englishText.classList.add('opacity-0');
        verbGroupDisplay.innerText = "";
        ieltsQuestion.style.display = 'none';
        ieltsAnswer.style.display = 'none';
        ieltsSynonyms.style.display = 'none';
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
        ieltsSynonyms.style.display = showTranslation ? 'block' : 'none';
        
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
          
          // Generate synonyms section
          if (currentCard.advancedVocab) {{
            const synonymsHtml = generateSynonymsSection(currentCard.advancedVocab);
            ieltsSynonyms.innerHTML = synonymsHtml;
          }} else {{
            ieltsSynonyms.innerHTML = '';
          }}
        }}
        cardCounter.innerText = `${{cardIndex + 1}}/${{filteredData.length}}`;
        return;
      }}
      
      // Regular cards (sentences, vocabulary, phrasal verbs)
      ieltsQuestion.style.display = 'none';
      ieltsAnswer.style.display = 'none';
      ieltsSynonyms.style.display = 'none';
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
