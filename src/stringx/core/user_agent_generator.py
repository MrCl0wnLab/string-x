"""
Módulo otimizado para geração de User-Agents aleatórios.

Este módulo fornece uma classe para gerar User-Agents para diferentes plataformas:
desktop, Linux, Mac, mobile e Windows, sem depender de arquivos externos.
Os user-agents gerados são randomizados mas mantêm formatos válidos para diferentes
navegadores e plataformas, incluindo Chrome, Firefox, Safari, Edge e Opera.
"""
import random
from typing import Dict, List, Union


class UserAgentGenerator:
    """
    Classe otimizada para geração de User-Agents aleatórios.
    
    Gera User-Agents para diferentes plataformas sem depender de arquivos externos.
    """
    # Dados de versões para navegadores, sistemas operacionais, etc.
    VERSIONS = {
        'chrome': ['88.0.4324.150', '89.0.4389.82', '90.0.4430.85', '95.0.4638.69'],
        'firefox': ['86.0', '89.0', '91.0', '92.0'],
        'edge': ['88.0.705.63', '90.0.818.46', '92.0.902.67'],
        'opera': ['74.0.3911.160', '76.0.4017.123', '77.0.4054.146'],
        'safari': ['14.0', '14.1', '15.0'],
        'webkit': ['605.1.15', '605.3.8', '612.1.29'],
        'webkit_linux': ['537.36', '538.1', '537.4'],
        'win': ['10.0', '6.3', '6.2', '6.1'],
        'mac': ['10_15_7', '11_1', '11_4', '12_0'],
        'android': ['9', '10', '11', '12'],
        'ios': ['14_5', '15_0', '15_2'],
        'wp_android': ['7.0', '8.0', '8.1']
    }
    
    # Modelos de dispositivos móveis
    MOBILE_MODELS = {
        'samsung': ['SM-G975F', 'SM-G991U', 'SM-G998B'],
        'google': ['Pixel 4', 'Pixel 5', 'Pixel 6'],
        'oneplus': ['OnePlus 9 Pro', 'OnePlus 10 Pro'],
        'xiaomi': ['Redmi Note 10 Pro', 'Mi 11'],
        'microsoft': ['NOKIA Lumia 950', 'Microsoft Lumia 650']
    }
    
    # Configurações adicionais
    WOW64_OPTIONS = ['Win64; x64', 'WOW64']
    LINUX_DISTROS = ['Ubuntu 20.04', 'Fedora 34', 'Debian 10']
    LINUX_ARCHS = ['x86_64', 'i686', 'aarch64']
    IOS_BUILD_IDS = ['18E148', '19A346', '19C56']
    
    # Templates para formato de User-Agent por plataforma e navegador
    BROWSER_TEMPLATES = {
        # Desktop
        'desktop_chrome': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver}',
        'desktop_firefox': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}',
        'desktop_edge': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} Edg/{edge_ver}',
        'desktop_safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Version/{safari_ver} Safari/{webkit_ver}',
        'desktop_opera': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} OPR/{opera_ver}',
        
        # Linux
        'linux_chrome': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver}',
        'linux_firefox': 'Mozilla/5.0 (X11; Linux {arch}; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}',
        'linux_opera': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} OPR/{opera_ver}',
        'linux_chrome_arch': 'Mozilla/5.0 (X11; {distro} {arch}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver}',
        'linux_generic': 'Mozilla/5.0 (X11; Linux {arch}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Version/{version} Chrome/{chrome_ver} Safari/{webkit_ver}',
        
        # Mac
        'mac_chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver}',
        'mac_firefox': 'Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}',
        'mac_safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Version/{safari_ver} Safari/{webkit_ver}',
        'mac_opera': 'Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} OPR/{opera_ver}',
        
        # Mobile
        'mobile_android': 'Mozilla/5.0 (Linux; Android {android_ver}; {model}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/{webkit_ver}',
        'mobile_ios': 'Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Version/{safari_ver} Mobile/{build_id} Safari/{webkit_ver}',
        'mobile_windows': 'Mozilla/5.0 (Windows Phone {android_ver}; Android {android_ver}; {model}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} Edge/{edge_ver} Mobile',
        
        # Windows
        'windows_chrome': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver}',
        'windows_firefox': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}',
        'windows_edge': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} Edg/{edge_ver}',
        'windows_ie': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}; Trident/7.0; rv:11.0) like Gecko',
        'windows_opera': 'Mozilla/5.0 (Windows NT {win_ver}; {wow64}) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_ver} OPR/{opera_ver}',
    }
    
    @classmethod
    def random_value_from_dict(cls, dict_key: str) -> str:
        """
        Método auxiliar para obter um valor aleatório do dicionário de versões.
        
        Args:
            dict_key (str): Chave para acessar o dicionário de versões (como 'chrome', 'firefox', etc.)
            
        Returns:
            str: Um valor aleatório do dicionário de versões para a chave especificada
            
        Examples:
            >>> UserAgentGenerator.random_value_from_dict('chrome')
            '89.0.4389.82'
        """
        return random.choice(cls.VERSIONS[dict_key])
    
    @classmethod
    def get_random_model(cls, brand_type: Union[str, List[str]]=None) -> str:
        """
        Retorna um modelo aleatório de dispositivo móvel.
        
        Args:
            brand_type (Union[str, List[str]], optional): Uma marca específica ou lista de marcas
                para selecionar o modelo. Se None, escolhe de todas as marcas disponíveis.
                
        Returns:
            str: Nome do modelo de dispositivo móvel
            
        Examples:
            >>> UserAgentGenerator.get_random_model('samsung')
            'SM-G975F'
            >>> UserAgentGenerator.get_random_model(['google', 'oneplus'])
            'Pixel 5'
        """
        if brand_type:
            if isinstance(brand_type, list):
                brand = random.choice(brand_type)
            else:
                brand = brand_type
            return random.choice(cls.MOBILE_MODELS[brand])
        
        # Selecione uma marca aleatória e depois um modelo dessa marca
        all_models = []
        for models in cls.MOBILE_MODELS.values():
            all_models.extend(models)
        return random.choice(all_models)
        
    @classmethod
    def get_desktop_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório para navegadores desktop.

        Returns:
            str: String de User-Agent para desktop
        """
        desktop_types = [
            'desktop_chrome', 'desktop_firefox', 'desktop_edge', 
            'desktop_safari', 'desktop_opera'
        ]
        browser_type = random.choice(desktop_types)
        template = cls.BROWSER_TEMPLATES[browser_type]
        
        # Preparar dados para formatação
        data = {
            'chrome_ver': cls.random_value_from_dict('chrome'),
            'firefox_ver': cls.random_value_from_dict('firefox'),
            'edge_ver': cls.random_value_from_dict('edge'),
            'opera_ver': cls.random_value_from_dict('opera'),
            'safari_ver': cls.random_value_from_dict('safari'),
            'webkit_ver': cls.random_value_from_dict('webkit'),
            'win_ver': cls.random_value_from_dict('win'),
            'mac_ver': cls.random_value_from_dict('mac'),
            'wow64': random.choice(cls.WOW64_OPTIONS)
        }
        
        return template.format(**data)

    @classmethod
    def get_linux_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório para sistemas Linux.

        Returns:
            str: String de User-Agent para Linux
        """
        linux_types = [
            'linux_chrome', 'linux_firefox', 'linux_opera', 
            'linux_chrome_arch', 'linux_generic'
        ]
        browser_type = random.choice(linux_types)
        template = cls.BROWSER_TEMPLATES[browser_type]
        
        # Versões genéricas para Linux
        versions = ['4.0.0', '5.0.0', '5.1.0', '6.0.0']
        
        # Preparar dados para formatação
        data = {
            'chrome_ver': cls.random_value_from_dict('chrome'),
            'firefox_ver': cls.random_value_from_dict('firefox'),
            'opera_ver': cls.random_value_from_dict('opera'),
            'webkit_ver': cls.random_value_from_dict('webkit_linux'),
            'version': random.choice(versions),
            'arch': random.choice(cls.LINUX_ARCHS),
            'distro': random.choice(cls.LINUX_DISTROS)
        }
        
        return template.format(**data)

    @classmethod
    def get_mac_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório para sistemas Mac OS.

        Returns:
            str: String de User-Agent para Mac OS
        """
        mac_types = [
            'mac_chrome', 'mac_firefox', 'mac_safari', 'mac_opera'
        ]
        browser_type = random.choice(mac_types)
        template = cls.BROWSER_TEMPLATES[browser_type]
        
        # Preparar dados para formatação
        data = {
            'mac_ver': cls.random_value_from_dict('mac'),
            'chrome_ver': cls.random_value_from_dict('chrome'),
            'firefox_ver': cls.random_value_from_dict('firefox'),
            'safari_ver': cls.random_value_from_dict('safari'),
            'webkit_ver': cls.random_value_from_dict('webkit'),
            'opera_ver': cls.random_value_from_dict('opera')
        }
        
        return template.format(**data)

    @classmethod
    def get_mobile_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório para dispositivos móveis.

        Returns:
            str: String de User-Agent para dispositivos móveis
        """
        mobile_types = ['mobile_android', 'mobile_ios', 'mobile_windows']
        platform_type = random.choice(mobile_types)
        template = cls.BROWSER_TEMPLATES[platform_type]
        
        # Preparar dados para formatação com valores padrão
        data = {
            'android_ver': cls.random_value_from_dict('android'),
            'ios_ver': cls.random_value_from_dict('ios'),
            'chrome_ver': cls.random_value_from_dict('chrome'),
            'firefox_ver': cls.random_value_from_dict('firefox'),
            'safari_ver': cls.random_value_from_dict('safari'),
            'webkit_ver': cls.random_value_from_dict('webkit'),
            'edge_ver': cls.random_value_from_dict('edge'),
            'opera_ver': cls.random_value_from_dict('opera'),
            'build_id': random.choice(cls.IOS_BUILD_IDS),
            'model': 'Unknown'  # Valor padrão, será atualizado abaixo
        }
        
        # Adicionar modelo específico de acordo com o tipo
        if platform_type == 'mobile_android':
            data['model'] = cls.get_random_model(['samsung', 'google', 'oneplus', 'xiaomi'])
        elif platform_type == 'mobile_windows':
            data['model'] = cls.get_random_model('microsoft')
            data['android_ver'] = cls.random_value_from_dict('wp_android')
        else:  # iOS
            data['model'] = 'iPhone'
        
        return template.format(**data)

    @classmethod
    def get_windows_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório para sistemas Windows.

        Returns:
            str: String de User-Agent para Windows
        """
        windows_types = [
            'windows_chrome', 'windows_firefox', 'windows_edge',
            'windows_ie', 'windows_opera'
        ]
        browser_type = random.choice(windows_types)
        template = cls.BROWSER_TEMPLATES[browser_type]
        
        # Preparar dados para formatação
        data = {
            'win_ver': cls.random_value_from_dict('win'),
            'wow64': random.choice(cls.WOW64_OPTIONS),
            'chrome_ver': cls.random_value_from_dict('chrome'),
            'firefox_ver': cls.random_value_from_dict('firefox'),
            'edge_ver': cls.random_value_from_dict('edge'),
            'opera_ver': cls.random_value_from_dict('opera'),
            'webkit_ver': cls.random_value_from_dict('webkit')
        }
        
        return template.format(**data)

    @classmethod
    def get_random_user_agent(cls) -> str:
        """
        Gera um User-Agent aleatório de qualquer categoria.
        
        Este método escolhe aleatoriamente entre todas as categorias disponíveis
        (desktop, Linux, Mac, mobile, Windows) e gera um User-Agent apropriado.

        Returns:
            str: String de User-Agent aleatório de qualquer plataforma
            
        Examples:
            >>> UserAgentGenerator.get_random_user_agent()
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        """
        methods = [
            cls.get_desktop_user_agent,
            cls.get_linux_user_agent,
            cls.get_mac_user_agent,
            cls.get_mobile_user_agent,
            cls.get_windows_user_agent
        ]
        
        selected_method = random.choice(methods)
        return selected_method()

    @classmethod
    def get_random_lib(cls) -> str:
        """
        Generates a random user agent string mimicking the format of various software versions.

        The user agent string is composed of:
        - Lynx version: Lynx/x.y.z where x is 2-3, y is 8-9, and z is 0-2
        - libwww version: libwww-FM/x.y where x is 2-3 and y is 13-15
        - SSL-MM version: SSL-MM/x.y where x is 1-2 and y is 3-5
        - OpenSSL version: OpenSSL/x.y.z where x is 1-3, y is 0-4, and z is 0-9

        Returns:
            str: A randomly generated user agent string.
        """
        lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
        libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
        ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
        openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
        return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"