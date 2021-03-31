Works best with English pdf

Usage :
*pip install pyaudiobook*

*import pyaudiobook*

*pyaudiobook.Pdf2Mp3(input_file_path,language="en",out_path = output_file_path,out_name=output_file_name,NumThreads=1)*

Language,out_path and out_name are optional.

Default Language : English

Default Output Path : User Home Directory

Default Output File Name : Output_timestamp

eg :
*convertor = pyaudiobook.Pdf2Mp3("sample.pdf",language="hi",out_path = '~/MyBooks',out_name='History of India',NumThreads=8)*
*print(convertor.output) #To get Output Filename*


Language Supported


    {
        "af": "Afrikaans",
        "ar": "Arabic",
        "bn": "Bengali",
        "bs": "Bosnian",
        "ca": "Catalan",
        "cs": "Czech",
        "cy": "Welsh",
        "da": "Danish",
        "de": "German",
        "el": "Greek",
        "en": "English",
        "eo": "Esperanto",
        "es": "Spanish",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "gu": "Gujarati",
        "hi": "Hindi",
        "hr": "Croatian",
        "hu": "Hungarian",
        "hy": "Armenian",
        "id": "Indonesian",
        "is": "Icelandic",
        "it": "Italian",
        "ja": "Japanese",
        "jw": "Javanese",
        "km": "Khmer",
        "kn": "Kannada",
        "ko": "Korean",
        "la": "Latin",
        "lv": "Latvian",
        "mk": "Macedonian",
        "ml": "Malayalam",
        "mr": "Marathi",
        "my": "Myanmar (Burmese)",
        "ne": "Nepali",
        "nl": "Dutch",
        "no": "Norwegian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "si": "Sinhala",
        "sk": "Slovak",
        "sq": "Albanian",
        "sr": "Serbian",
        "su": "Sundanese",
        "sv": "Swedish",
        "sw": "Swahili",
        "ta": "Tamil",
        "te": "Telugu",
        "th": "Thai",
        "tl": "Filipino",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "vi": "Vietnamese",
        "zh-CN": "Chinese",
    }
