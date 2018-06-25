# coding: utf-8

# ******************************* 
# 
# Nome do projeto: Data Cleansing Release
# Versao do arquivo: 1.0
# Data da criação do arquivo: 01/02/2017 04:36:23
# 
# ******************************* 

import unicodedata, sys, re, codecs, os
from unicodedata import normalize

# ------------------------------ 
# CLASSES / IMPORTACOES

class limpador_de_texto():

	parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	sys.path.append(os.path.join(parentdir, "model"))
	#import unicodedata
	class LimpadorDeTexto(object):
	    def __init__(self):
	        self.regexDF = re.compile(u'.*?(?P<separador>((DF)|(D[IíÍ]ST(R([IíÍ]TO)?)? FED(ERAL)?)))')
	        ''' por incrivel que pareça os hifens são diferêntes, mantenha os 2 '''
	        self.finalizadoresDeLogradouro = u'([\\\\\\(])|( \\–)|( \\-)|(\\– )|(\\- )|(–[ ,\\-\\.|]*$)|(-[ ,\\–\\.|]*$)|S\/(?=N\W)|,(?![\s]*RUA)'
	        self.finalizadoresDeLogradouroRegex = re.compile('.*?[\w]+.*?(?P<separador>('+self.finalizadoresDeLogradouro+'))')
	        ''' identificadores que o endereço não tem número, exemplo S/N '''
	        self.regexIdentificadoresSemNumero = re.compile(u'.*?(?P<separador>((^| )S(EM)?[ \\-_\\.\\\\/]?N([UúÚ]MERO|[°ººª])?([\\W]|$))|( S[\\. ]?N))')
	        self.limpaNumeroRegex = re.compile( u'.*?(?P<order>[0-9]+)')
	        self.limpaNumeroDecimalRegex = re.compile( u'.*?(?P<order>[0-9]+([\\.,]?[0-9]+)*)')
	        self.limpaNumeroLetraRegex = re.compile( u'.*?(?P<order>(([0-9]+([\\–\\-]?[\\w])?)|([\\w]$)))')
	        self.limpaNumeroLetraDecimalRegex = re.compile( u'.*?(?P<order>(([0-9]+([\\.,]?[0-9]+)*([\\–\\-]?[\\w])?)|([\\w]$)))')
	        self.regexUf = u'(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
	        self.compiledRegexUfInicio = re.compile(u'(?P<separador>('+self.regexUf+u'|(BR))[ \\-\\–]{0,3}[\d]+)')
	        self.separadorNumeroDepoisDeNumero = re.compile(u'.*?[\d]+[ ](?P<order>[0-9]+)')
	        self.regexNumeroIndependenteDoSeparador = re.compile(u'.*?\D(?P<order>[0-9]+)')
	        ''' Em Brasilia, busca o ultimo numero de uma string '''
	        self.regexNumeroIndependenteDoSeparadorDF = re.compile(u'.*?\D(?P<order>([0-9]+(?=[^0-9]*$))|(\d+(?=\/[\w]+)))')
	    def limparNumero(self, numero, removerDecimais):
	        if (numero != None):
	            if (removerDecimais):
	                encontrado = self.limpaNumeroRegex.match(numero)
	            else:
	                encontrado = self.limpaNumeroDecimalRegex.match(numero)
	            if (encontrado != None):
	                primeiroDigito = encontrado.group('order');
	                if (len(primeiroDigito) > 0):
	                    return primeiroDigito.replace('.', '')
	        return None
	    def limparNumeroLetra(self, valorALimpar, removerDecimais):
	        # print 'Valor A Limpar:', valorALimpar
	        if (valorALimpar != None):
	            if (removerDecimais):
	                encontrado = self.limpaNumeroLetraRegex.match(valorALimpar)
	            else:
	                encontrado = self.limpaNumeroLetraDecimalRegex.match(valorALimpar)
	            if (encontrado != None):
	                primeiroDigito = encontrado.group('order');
	                if (len(primeiroDigito) > 0):
	                    valorLimpo = primeiroDigito
	                    if (removerDecimais):
	                        valorLimpo = valorLimpo.replace('.', '')
	                    # print 'Valor Limpo:', valorLimpo
	                    return valorLimpo
	        return None
	    def limparLogradouro(self, logradouro):
	        final = None
	        encontrado = self.finalizadoresDeLogradouroRegex.match(logradouro.upper())
	        if (encontrado != None):
	            inicio = encontrado.start('separador')
	            if (inicio != -1 and (final == None or inicio < final)):
	                final = inicio
	        if (final != None):
	            logradouro = logradouro[:final]
	        logradouro = logradouro.strip()
	        encontrado = self.compiledRegexUfInicio.match(logradouro.upper())
	        if (encontrado != None):
	            final = encontrado.end('separador')
	            logradouro = logradouro[:final].strip()
	        ''' Para endereços de Brasilia '''
	        logradouro = re.sub(',', ' ', logradouro)
	        logradouro = re.sub('(\\.)(\\w)', '. \\2', logradouro)
	        logradouro = re.sub('  ', ' ', logradouro)
	        logradouro = re.sub('\*[ ]*', '', logradouro)
	        return logradouro
	    def limparLogradouroDF_Preparacao(self, logradouro):
	        if (logradouro != None):
	            logradouro = re.sub('Q C[\d ]', 'QC ', logradouro)
	            logradouro = re.sub(',(?=\d)', ', ', logradouro)
	            logradouro = re.sub('(?<=\d\d\d)\/(?=\d\d\d)', ' ', logradouro)
	        return logradouro   
	    def limparLogradouroDF_Montagem(self, logradouro):
	        if (logradouro != None):
	            logradouro = re.sub('(\. )(?=\w[\. \/])', '', logradouro)
	            logradouro = re.sub('[*]*[(]*[)]*', '', logradouro)
	            logradouro = re.sub('(\/)|(\. )(?=\w\w)', ' ', logradouro)
	            logradouro = re.sub('[^A-z0-9]', ' ', logradouro)
	            logradouro = re.sub('  ', ' ', logradouro)
	        return logradouro
	    def limparCep(self, cep):
	        cep = unicodedata.normalize('NFKD', unicode(cep)).encode('ASCII', 'ignore')
	        return re.sub('\\D', '', cep)
	    # retorna uma instancia de FinalDoLogradouro com o indice onde o endereço acaba e dizendo se é sem número
	    # retorna None se numero ou anotação de sem numero não for encontrada
	    def encontrarFinalDoLogradouro(self, enderecoDividido):
	        if (enderecoDividido.tipoDeLogradouro == 'RODOVIA' or enderecoDividido.tipoDeLogradouro == 'ESTRADA'):
	            offset = 3
	        else:
	            offset = 1
	        # limpa endereço apenas para tratamento interno
	        endLimpo = re.sub(u'^[/\\\\\.:\\-, "\']+', '', enderecoDividido.logradouro)
	        diffLenLimpo = len(enderecoDividido.logradouro) - len(endLimpo)
	        enderecoMaiusculo = endLimpo.upper()
	        # Verifica se é sem numero, se for ja retorna
	        encontrado = self.regexIdentificadoresSemNumero.match(enderecoMaiusculo)
	        if (encontrado != None):
	            return final_do_logradouro.FinalDoLogradouro(encontrado.start('separador')+diffLenLimpo, True)
	        # tenta achar o numero pelo separador
	        final = None
	        #encontra numero depois do numero (rua pio 12 7)
	        encontrado = self.separadorNumeroDepoisDeNumero.match(enderecoMaiusculo[offset:])
	        if (encontrado != None):
	            inicioReal = encontrado.start('order')+offset+diffLenLimpo
	            if (final == None or inicioReal < final):
	                final = inicioReal;
	                return final_do_logradouro.FinalDoLogradouro(final, False);
	        # encontra numero independente de separador
	        # brasilia
	        if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) != None):
	            encontrado = self.regexNumeroIndependenteDoSeparadorDF.match(enderecoMaiusculo[offset:])
	        else:
	            encontrado = self.regexNumeroIndependenteDoSeparador.match(enderecoMaiusculo[offset:])
	        # nao-brasilia
	        if (encontrado != None):
	            inicioReal = encontrado.start('order')+offset+diffLenLimpo
	            if (final == None or inicioReal < final):
	                final = inicioReal;
	        #retorna o final caso ele exista
	        if (final != None):
	            return final_do_logradouro.FinalDoLogradouro(final, False);
	        # print u'nao achou:' + enderecoMaiusculo
	        return None
	    def removerAcentos(self, input_str):
	        if (input_str != None):
	            try:
	                outputStr = normalize('NFKD', input_str).encode('ASCII','ignore')
	            except:
	                outputStr = input_str.decode('utf-8')
	                outputStr = normalize('NFKD', outputStr).encode('ASCII','ignore')
	            return outputStr
	        else:
	            return None

class logradouro_numero():

	class LogradouroNumero(object):
	    def __init__(self, logradouro, numero, cidade, uf):
	        self.logradouro = logradouro
	        self.numero = numero
	        self.apartamento = None
	        self.bloco = None
	        self.lote = None
	        self.quadra = None
	        self.trecho = None
	        self.areaEspecial = None
	        self.comercioLocal = None
	        self.casa = None
	        self.casaSemAbreviacao = None
	        self.bairro = None
	        self.andar = None
	        self.sala = None
	        self.caixaPostal = None
	        self.kilometro = None
	        self.conjunto = None
	        self.loja = None
	        self.setor = None
	        self.tipoDeLogradouro = None
	        self.modulo = None
	        self.cidade = cidade
	        self.uf = uf
	        ''' complemento residual ex: fundos '''
	        self.complemento = None
	        self.titulo = None
	        self.cep = None
	        self.subsolo = None
	        self.inputLimpo = None
	    def equal(self, other):
	        return self.__dict__ == other.__dict__
	    def __eq__(self, other):
	        return self.__dict__ == other.__dict__

class tipo_de_logradouro_resposta():

	class TipoDeLogradouroResposta(object):
	    def __init__(self, indiceInicio, indiceFim, tipoDeLogradouro, tipoDeLogradouroEncontrado, inferido):
	        self.indiceInicio = indiceInicio
	        self.indiceFim = indiceFim
	        self.tipoDeLogradouro = tipoDeLogradouro
	        self.tipoDeLogradouroEncontrado = tipoDeLogradouroEncontrado
	        self.inferido = inferido

class localizador_tipo_de_logradouro():

	#from model.separador_de_numero import SeparadorDeNumero
	parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	sys.path.append(os.path.join(parentdir, "model"))
	class LocalizadorTipoDeLogradouro(object):
	    def __init__(self):
	        self.regexDF = re.compile(u'.*?(?P<separador>((DF)|(D[IíÍ]ST(R([IíÍ]TO)?)? FED(ERAL)?)))')
	        ''' identificadores do tipo de logradouro ex: rua, travessa, rotatória... '''
	        self.tiposDeLogradouro = []
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PRIMEIRA RUA', [u'((1[\.°ººª/\\\\:\-, ]{0,2})|(PRI(M(EIRA)?)?[\\.,\-]?))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEGUNDA RUA', [u'((2[\.°ººª/\\\\:\-, ]{0,2})|(SEGUNDA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'TERCEIRA RUA', [u'((3[\.°ººª/\\\\:\-, ]{0,2})|(TERCEIRA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUARTA RUA', [u'((4[\.°ººª/\\\\:\-, ]{0,2})|(QUARTA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUINTA RUA', [u'((5[\.°ººª/\\\\:\-, ]{0,2})|(QUINTA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEXTA RUA', [u'((6[\.°ººª/\\\\:\-, ]{0,2})|(SEXTA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SÉTIMA RUA', [u'((7[\.°ººª/\\\\:\-, ]{0,2})|(S[EéÉ]TIMA))[ ]?RUA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'AVENIDA', [u'(RUA )*((AVENIDA)|(AV(E){0,1}))'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'ESTRADA MUNICIPAL', [u'ES(T(R(ADA)?)?)? M(U(N(IC(IPAL)?)?)?)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'ESTRADA', [u'ES(T(R(ADA)?)?)?','(RUA )*EST(R(A(D(A)?)?)?)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RUA', [u'R(U[A]?)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PRIMEIRA AVENIDA', [u'((1[\.°ººª/\\\\:\-, ]{0,2})|(PRI(M(EIRA)?)?[\\.,\-]?))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEGUNDA AVENIDA', [u'((2[\.°ººª/\\\\:\-, ]{0,2})|(SEGUNDA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'TERCEIRA AVENIDA', [u'((3[\.°ººª/\\\\:\-, ]{0,2})|(TERCEIRA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUARTA AVENIDA', [u'((4[\.°ººª/\\\\:\-, ]{0,2})|(QUARTA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUINTA AVENIDA', [u'((5[\.°ººª/\\\\:\-, ]{0,2})|(QUINTA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEXTA AVENIDA', [u'((6[\.°ººª/\\\\:\-, ]{0,2})|(SEXTA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SÉTIMA AVENIDA', [u'((7[\.°ººª/\\\\:\-, ]{0,2})|(S[EéÉ]TIMA))[ ]?AVENIDA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'AVENIDA', [u'((AVENIDA)|(AV(E){0,1}))'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'ALAMEDA', [u'AL(AMEDA)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PRACA CÍVICA', [u'P(RA)?[CÇç][A]? C[ÍIí]VICA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PRACA', [u'P(RA)?[CÇç][A]?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RODOANEL', [u'(((ROD(OVIA)?)|(VIA)) )?RODOANEL'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RODOVIA', [u'((ROD(OVIA)?)|(VIA))'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'GALERIA', [u'GAL(ERIA)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'LAGOA', [u'LAGOA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'LAGO', [u'L[A]?G[O]?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'VIELA', [u'VIELA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'TUNEL', [u'T[UúÚ]?N(EL)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'BALNEÁRIO', [u'BAL(NE[ÁAá]RIO)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RAMAL', [u'RAMAL'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PRIMEIRA TRAVESSA', [u'((1[\.°ººª/\\\\:\-, ]{0,2})|(PRI(M(EIRA)?)?[\\.,\-]?))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEGUNDA TRAVESSA', [u'((2[\.°ººª/\\\\:\-, ]{0,2})|(SEGUNDA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'TERCEIRA TRAVESSA', [u'((3[\.°ººª/\\\\:\-, ]{0,2})|(TERCEIRA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUARTA TRAVESSA', [u'((4[\.°ººª/\\\\:\-, ]{0,2})|(QUARTA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'QUINTA TRAVESSA', [u'((5[\.°ººª/\\\\:\-, ]{0,2})|(QUINTA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SEXTA TRAVESSA', [u'((6[\.°ººª/\\\\:\-, ]{0,2})|(SEXTA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'SÉTIMA TRAVESSA', [u'((7[\.°ººª/\\\\:\-, ]{0,2})|(S[EéÉ]TIMA))[ ]?TRAVESSA'], False))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'TRAVESSA', [u'T(R(A)?)?V(ESSA)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'BECO', [u'BECO'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'ACESSO', [u'ACESSO'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'CAMINHO', [u'CAMINHO'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'LADEIRA', [u'LADEIRA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'LARGO', [u'LARGO'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'MARGINAL', [u'MARGINAL'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PASSAGEM', [u'P(A)?SS(AGEM)?'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'VIA', [u'VIA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'PONTE', [u'P(ON)?TE'], True))
			# removido por causa de Brasília, estava em conflito com o ajuste com nomes invertidos "josé de abreu, rua"
	        # self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'Quadra', [u'QUADRA'], True))
	        self.tiposDeLogradouro.append(tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'VIADUTO', [u'V(IA)?D(UTO)?'], True))
	        self.tiposDeLogradouroInicioRE = []
	        self.tiposDeLogradouroQualquerRE = []
	        self.tiposDeLogradouroAposVirgulaRE = []
	        for tipoDeLogradouro in self.tiposDeLogradouro:
	            for alias in tipoDeLogradouro.aliases:
	                self.tiposDeLogradouroInicioRE.append([tipoDeLogradouro, re.compile(u'('+alias+u'[/\\\\\.:\\-, \\d]+)*(?P<order>'+alias+u')[/\\\\\.:\\-, \\d]+', re.UNICODE)])
	                self.tiposDeLogradouroQualquerRE.append([tipoDeLogradouro, re.compile(u'((.*[ \\-\\_\\\\/\\.,])|(^))(?P<order>'+alias+u')[/\\\\\.:\-, ]+')])
	                self.tiposDeLogradouroAposVirgulaRE.append([tipoDeLogradouro, re.compile(u'.*[\\,][ ]?(?P<order>'+alias+u')[/\\\\\.:\-, ]+')])
	        self.regexUf = u'(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
	        self.compiledRegexUfInicio = re.compile(u'(?P<separador>('+self.regexUf+u'|(BR))[ \\-\\–]{0,3}\d)')
	        self.compiledRegexUfQualquer = re.compile(u'.+[ \\-_\\\\/\\.,](?P<separador>('+self.regexUf+u'|(BR))[ \\-\\–]{0,3}\d)')
	    def encontrarTipoDeLogradouroNoComeco(self, enderecoMaiusculo, uf=None):
	        # soma ao offset o tamanho do tipo de logradouro caso exista
	        for compiledAlias in self.tiposDeLogradouroInicioRE:
	            encontrado = compiledAlias[1].match(enderecoMaiusculo)
	            if (encontrado != None):
	                return tipo_de_logradouro_resposta.TipoDeLogradouroResposta(encontrado.start('order'), encontrado.end('order'), compiledAlias[0], encontrado.group('order'), False)
	        if (uf != None and self.regexDF.match(uf) != None and enderecoMaiusculo[:2] != "DF"):
	            return None
	        encontrado = self.compiledRegexUfInicio.match(enderecoMaiusculo.upper())
	        if (encontrado != None):
	            return tipo_de_logradouro_resposta.TipoDeLogradouroResposta(0, 0, tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RODOVIA', None, True), u'', True)
	        return None
	    def encontrarTipoDeLogradouroIndependenteDoLugar(self, enderecoMaiusculo):
			# soma ao offset o tamanho do tipo de logradouro caso exista
	        finalEncontrado =  None
	        inicioEncontrado =  None
	        aliasEncontrado = None
	        for compiledAlias in self.tiposDeLogradouroQualquerRE:
	            encontrado = compiledAlias[1].match(enderecoMaiusculo)
	            if (encontrado != None and (finalEncontrado == None or encontrado.end('order') < finalEncontrado)):
	                inicioEncontrado = encontrado.start('order')
	                finalEncontrado = encontrado.end('order')
	                valorEncontrado = encontrado.group('order')
	                aliasEncontrado = compiledAlias[0]
	        if (finalEncontrado != None):
	            return tipo_de_logradouro_resposta.TipoDeLogradouroResposta(inicioEncontrado, finalEncontrado, aliasEncontrado, valorEncontrado, False)
	        encontrado = self.compiledRegexUfQualquer.match(enderecoMaiusculo.upper())
	        if (encontrado != None):
	            return tipo_de_logradouro_resposta.TipoDeLogradouroResposta(encontrado.start('separador'), encontrado.start('separador'), tipo_de_logradouro_com_aliases.TipoDeLogradouroComAliases(u'RODOVIA', None, True), u'', True)
	        return None
	    def encontrarTipoDeLogradouroAposVirgula(self, enderecoMaiusculo):
			# soma ao offset o tamanho do tipo de logradouro caso exista
	        finalEncontrado =  None
	        inicioEncontrado =  None
	        aliasEncontrado = None
	        for compiledAlias in self.tiposDeLogradouroAposVirgulaRE:
	            encontrado = compiledAlias[1].match(enderecoMaiusculo)
	            if (encontrado != None and (finalEncontrado == None or encontrado.end('order') < finalEncontrado)):
	                inicioEncontrado = encontrado.start('order')
	                finalEncontrado = encontrado.end('order')
	                valorEncontrado = encontrado.group('order')
	                aliasEncontrado = compiledAlias[0]
	        if (finalEncontrado != None):
	            return tipo_de_logradouro_resposta.TipoDeLogradouroResposta(inicioEncontrado, finalEncontrado, aliasEncontrado, valorEncontrado, False)
	        return None

class final_do_logradouro():

	class FinalDoLogradouro(object):
	    # indiceFim: numero inteiro, indice onde o logradouro acaba
	    # semNumero: booleano, True se ele é sem numero (tem ' s/n'), False se não se pode dizer que é sem numero
	    def __init__(self, indiceFim, semNumero):
	        self.indiceFim = indiceFim
	        self.semNumero = semNumero
	    def equal(self, other):
	        return isinstance(other, self.__class__) and (self.indiceFim == other.indiceFim and self.semNumero == other.semNumero)
	    def __eq__(self, other):
	        return isinstance(other, self.__class__) and (self.indiceFim == other.indiceFim and self.semNumero == other.semNumero)

class montador_de_endereco():

	class MontadorDeEndereco(object):
	    def __init__(self):
	        self.regexDF = re.compile(u'.*?(?P<separador>((DF)|(D[IíÍ]ST(R([IíÍ]TO)?)? FED(ERAL)?)))')
	        self.limpadorDeTexto = limpador_de_texto.LimpadorDeTexto()
	        self.cidadesComEnderecamentoEspecial = []
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'FORMOSA'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'GOI[AâÂ]NIA'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'LUZI[AâÂ]NIA'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'NOVO GAMA'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'PLANALTINA DE GOI[AáÁ]S'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'[AÁá]GUAS LINDAS DE GOI[AáÁ]S'])
	        self.cidadesComEnderecamentoEspecial.append([u'(GO)|(GOI[AáÁ]S)', u'VALPARAISO DE GOI[AáÁ]S'])
	        self.cidadesComEnderecamentoEspecial.append([u'(SP)|(S[AãÃ]O PAULO)', u'BAUR[UúÚ]'])
	        self.cidadesComEnderecamentoEspecial.append([u'(TO)|(TOCANTINS)', u'PALMAS'])
	    # retorna uma instancia de LogradouroNumero
	    def montarEndereco(self, enderecoSeparado):
	        if (enderecoSeparado.cidade != None and enderecoSeparado.uf != None):
	            for cidadeComEnderecamentoEspecial in self.cidadesComEnderecamentoEspecial:
	                encontrado = re.match(u'.*?(?P<separador>'+cidadeComEnderecamentoEspecial[1]+u'+)', enderecoSeparado.cidade.upper())
	                if (encontrado != None):
	                    estadoEncontrado = re.match(u'.*?(?P<separador>('+cidadeComEnderecamentoEspecial[0]+u')+)', enderecoSeparado.uf.upper())
	                    if (estadoEncontrado != None):
	                        return enderecoSeparado.inputLimpo
	        ''' Endereços de Brasilia '''
	        if (enderecoSeparado.uf != None and self.regexDF.match(enderecoSeparado.uf) != None):
	            enderecoSeparado.uf = "DF"
	            enderecoSeparado.cidade = "BRASILIA"
	            enderecoSeparado.logradouro = self.limpadorDeTexto.limparLogradouroDF_Montagem(enderecoSeparado.logradouro)
	            if (enderecoSeparado.numero != None):
	                enderecoSeparado.logradouro += " " + enderecoSeparado.numero
	            if (enderecoSeparado.setor != None):
	                enderecoSeparado.logradouro += " SETOR " + enderecoSeparado.setor
	            if (enderecoSeparado.trecho != None):
	                enderecoSeparado.logradouro += " TRECHO " + enderecoSeparado.trecho
	            if (enderecoSeparado.quadra != None):
	                enderecoSeparado.logradouro += " QUADRA " + enderecoSeparado.quadra
	            if (enderecoSeparado.comercioLocal != None):
	                enderecoSeparado.logradouro += " COMERCIO LOCAL " + enderecoSeparado.comercioLocal
	            if (enderecoSeparado.areaEspecial != None):
	                enderecoSeparado.logradouro += " AREA ESPECIAL " + enderecoSeparado.areaEspecial
	            if (enderecoSeparado.conjunto != None):
	                enderecoSeparado.logradouro += " CONJUNTO " + enderecoSeparado.conjunto
	            if (enderecoSeparado.bloco != None):
	                enderecoSeparado.logradouro += " BLOCO " + enderecoSeparado.bloco
	            if (enderecoSeparado.lote != None):
	                enderecoSeparado.logradouro += " LOTE " + enderecoSeparado.lote
	            enderecoSeparado.logradouro = re.sub(u'^[ ]+', '', enderecoSeparado.logradouro)
	            return enderecoSeparado.logradouro
	        ''' '''
	        if (enderecoSeparado.logradouro == None or enderecoSeparado.logradouro == ''):
	            return enderecoSeparado.inputLimpo
	        if (enderecoSeparado.numero != None):
	            return enderecoSeparado.logradouro + ", " + enderecoSeparado.numero
	        else:
	            return enderecoSeparado.logradouro

class identificador_secundario():

	class IdentificadorSecundario(object):
	    def __init__(self, identificador, regex):
	        self.identificador = identificador
	        self.regex = regex
	        self.aceitaLetras = True

class tipo_de_logradouro_com_aliases():

	class TipoDeLogradouroComAliases(object):
	    def __init__(self, tipoDeLogradouro, aliases, logradouroPrecisaTerNome):
	        self.tipoDeLogradouro = tipoDeLogradouro
	        self.aliases = aliases
	        self.logradouroPrecisaTerNome = logradouroPrecisaTerNome

class preparador_de_endereco():

	parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	sys.path.append(os.path.join(parentdir, "model"))
	sys.path.append(os.path.join(parentdir, "services"))
	class PreparadorDeEndereco(object):
	    def __init__(self):
	        self.regexDF = re.compile(u'.*?(?P<separador>((DF)|(D[IíÍ]ST(R([IíÍ]TO)?)? FED(ERAL)?)))')
	        self.localizadorTipoDeLogradouro = localizador_tipo_de_logradouro.LocalizadorTipoDeLogradouro()
	        self.limpadorDeTexto = limpador_de_texto.LimpadorDeTexto()
	        self.regexUf = u'(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
	        self.regexUfSigla = re.compile(u'.*[:\\\\/ ,\–\-\.| ]+(?P<order>'+self.regexUf+u')([:\\\\/ ,\\–\\-\\.|;]|(BR(A([ZS]IL)?)?))*$', re.UNICODE)
	        # self.regexUfCompleto = u'.*([:\\\\/ ,\–\-\.| ]+|^)'
	        # self.regexUfCompleto += u'((?P<AC>ACRE)'
	        # self.regexUfCompleto += u'|(?P<AL>ALAGOAS)'
	        # self.regexUfCompleto += u'|(?P<AP>AMAP[áÁA])'
	        # self.regexUfCompleto += u'|(?P<AM>AMA[ZS]ONA[SZ]?)'
	        # self.regexUfCompleto += u'|(?P<BA>BA[H]?[IY]A)'
	        # self.regexUfCompleto += u'|(?P<CE>CEAR[áÁA])'
	        # self.regexUfCompleto += u'|(?P<DF>DISTRITO FEDERAL)'
	        # self.regexUfCompleto += u'|(?P<ES>ESPIRITO SANTO)'
	        # self.regexUfCompleto += u'|(?P<GO>GOI[áÁA]S)'
	        # self.regexUfCompleto += u'|(?P<MA>MARANH[ãÃA]O)'
	        # self.regexUfCompleto += u'|(?P<MT>MATO GROSSO)'
	        # self.regexUfCompleto += u'|(?P<MS>MATO GROSSO (DO )?S(UL|[\\.]))'
	        # self.regexUfCompleto += u'|(?P<MG>MINAS GERAIS)'
	        # self.regexUfCompleto += u'|(?P<PA>PAR[áÁA])'
	        # self.regexUfCompleto += u'|(?P<PB>PAR[áÁA][H]?[IíÍY]BA)'
	        # self.regexUfCompleto += u'|(?P<PR>PARAN[áÁA])'
	        # self.regexUfCompleto += u'|(?P<PE>PERNAMBUCO)'
	        # self.regexUfCompleto += u'|(?P<PI>PIAU[íÍI])'
	        # self.regexUfCompleto += u'|(?P<RJ>RIO (DE )?JANE[I]?RO)'
	        # self.regexUfCompleto += u'|(?P<RN>RIO GRANDE DO NORTE)'
	        # self.regexUfCompleto += u'|(?P<RS>RIO GRANDE DO SUL)'
	        # self.regexUfCompleto += u'|(?P<RO>ROND[ôÔO]NIA)'
	        # self.regexUfCompleto += u'|(?P<RR>RORAIMA)'
	        # self.regexUfCompleto += u'|(?P<SC>SANTA CATARINA)'
	        # self.regexUfCompleto += u'|(?P<SP>S([AÃã]O|[\\.])( )?PAULO)'
	        # self.regexUfCompleto += u'|(?P<SE>SERGIPE)'
	        # self.regexUfCompleto += u'|(?P<TO>TOCANTINS))'
	        # self.regexUfCompleto += u'([:\\\\/ ,\\–\\-\\.|;]*(BR(A([ZS]IL)?)?)?)*$'
	        # self.regexUfCompleto = re.compile(self.regexUfCompleto, re.UNICODE);
	        # regex dividida para funcionar no .net
	        self.regexUfCompletoA = u'.*([:\\\\/ ,\–\-\.| ]+|^)'
	        self.regexUfCompletoA += u'((?P<AC>ACRE)'
	        self.regexUfCompletoA += u'|(?P<AL>ALAGOAS)'
	        self.regexUfCompletoA += u'|(?P<AP>AMAP[áÁA])'
	        self.regexUfCompletoA += u'|(?P<AM>AMA[ZS]ONA[SZ]?)'
	        self.regexUfCompletoA += u'|(?P<BA>BA[H]?[IY]A)'
	        self.regexUfCompletoA += u'|(?P<CE>CEAR[áÁA])'
	        self.regexUfCompletoA += u'|(?P<DF>DISTRITO FEDERAL)'
	        self.regexUfCompletoA += u'|(?P<ES>ESPIRITO SANTO)'
	        self.regexUfCompletoA += u'|(?P<GO>GOI[áÁA]S)'
	        self.regexUfCompletoA += u'|(?P<MA>MARANH[ãÃA]O))'
	        self.regexUfCompletoA += u'([:\\\\/ ,\\–\\-\\.|;]*(BR(A([ZS]IL)?)?)?)*$'
	        self.regexUfCompletoA = re.compile(self.regexUfCompletoA, re.UNICODE);
	        self.regexUfCompletoB = u'.*([:\\\\/ ,\–\-\.| ]+|^)'
	        self.regexUfCompletoB += u'((?P<MT>MATO GROSSO)'
	        self.regexUfCompletoB += u'|(?P<MS>MATO GROSSO (DO )?S(UL|[\\.]))'
	        self.regexUfCompletoB += u'|(?P<MG>MINAS GERAIS)'
	        self.regexUfCompletoB += u'|(?P<PA>PAR[áÁA])'
	        self.regexUfCompletoB += u'|(?P<PB>PAR[áÁA][H]?[IíÍY]BA)'
	        self.regexUfCompletoB += u'|(?P<PR>PARAN[áÁA])'
	        self.regexUfCompletoB += u'|(?P<PE>PERNAMBUCO)'
	        self.regexUfCompletoB += u'|(?P<PI>PIAU[íÍI])'
	        self.regexUfCompletoB += u'|(?P<RJ>RIO (DE )?JANE[I]?RO)'
	        self.regexUfCompletoB += u'|(?P<RN>RIO GRANDE DO NORTE))'
	        self.regexUfCompletoB += u'([:\\\\/ ,\\–\\-\\.|;]*(BR(A([ZS]IL)?)?)?)*$'
	        self.regexUfCompletoB = re.compile(self.regexUfCompletoB, re.UNICODE);
	        self.regexUfCompletoC = u'.*([:\\\\/ ,\–\-\.| ]+|^)'
	        self.regexUfCompletoC += u'((?P<RS>RIO GRANDE DO SUL)'
	        self.regexUfCompletoC += u'|(?P<RO>ROND[ôÔO]NIA)'
	        self.regexUfCompletoC += u'|(?P<RR>RORAIMA)'
	        self.regexUfCompletoC += u'|(?P<SC>SANTA CATARINA)'
	        self.regexUfCompletoC += u'|(?P<SP>S([AÃã]O|[\\.])( )?PAULO)'
	        self.regexUfCompletoC += u'|(?P<SE>SERGIPE)'
	        self.regexUfCompletoC += u'|(?P<TO>TOCANTINS))'
	        self.regexUfCompletoC += u'([:\\\\/ ,\\–\\-\\.|;]*(BR(A([ZS]IL)?)?)?)*$'
	        self.regexUfCompletoC = re.compile(self.regexUfCompletoC, re.UNICODE);
	        self.iniciaComNumeroRegex = re.compile(u'^[\W]*\d')
	        self.regexZeros = re.compile(u'^[0]*$')
	        self.diferenteDeNumeros = re.compile(u'^[\d]+$')
	        self.separadoresDeNumeroRegex = []
	        self.separadoresDeNumeroRegex.append(re.compile(u'.*?(N([ÚúU]M(E)?)?[R]?[O]?)[\\.Â°ººª/\\\\:\\-,]*[\D]?[\\d]+([\\.]+[\\d]+)*.*?(?P<order>(([\\\\/ ])+|^)(N([ÚúU]M(E)?)?[R]?[O]?)[\\.Â°ººª/\\\\:\\-,]*[\D]?[\\d]+([\\.]+[\\d]+)*)'))
	        self.separadoresDeNumeroRegex.append(re.compile(u'.*?(?P<order>(([\\\\/ ])+|^)(N([ÚúU]M(E)?)?[R]?[O]?)[\\.Â°ººª/\\\\:\\-,]*[\D]?[\\d]+([\\.]+[\\d]+)*)'))
	        self.separadoresDeNumeroRegex.append(re.compile(u'.*?(?P<order>[,][\D]?[\d]+([\.]+[\d]+)*)'))
	        ''' identificadores de dados complementates do entereço (fora nome do logradoro e número) '''
	        self.identificadoresSecundariosNumericos = []
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'casa', u'(CASAS|CASA|CS|C)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'casaSemAbreviacao', u'(CASAS|CASA)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'loja', u'(LOJA|LJ|LOJAS)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'trecho', u'(TRECHO|TR)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'areaEspecial', u'(AE|[ÁA]REA ESPECIAL|[ÁA]REAS ESPECIAIS)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'quadra', u'(QUADRA|QD|Q)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'comercioLocal', u'(COM[EÉ]RCIO LOCAL|CL)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'lote', u'(LOTE RURAL|LOTES|LOTE|LT|LTS|LTOES)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'apartamento', u'(APARTAMENTO|APTO|APT|AP)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'bloco', u'(BLOCO|BLOCOS|BL)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'conjunto', u'(CONJUNTO|CONJ|CJ)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'sala', u'(SALAS|SALA|SL|SLS|S/ )'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'kilometro', u'(((QU)|(K))ILOM[EêÊéÉ]TRO|KM)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'caixaPostal', u'(CAIXA POSTAL|CX.POSTAL)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'setor', u'(SETOR)'))
	        self.identificadoresSecundariosNumericos.append(identificador_secundario.IdentificadorSecundario(u'modulo', u'(M[OóÓ]DULO)'))
	        self.identificadoresSecundariosRE = []
	        for identificadorSecundario in self.identificadoresSecundariosNumericos:
	            self.identificadoresSecundariosRE.append([identificadorSecundario.identificador, re.compile(u'.*?([\\\\/:\\–\\-,_\\(\\)\\d ]|^)+(?P<order>'+identificadorSecundario.regex+u'((((N[úÚU]MERO)|([°ºª\\.\\\\:/\\-, ])|([\W]N(?!N)))*[0-9]+([\\.,]?[0-9])*([\\–\\-]?[\\w])?)|([°ºª\\.\\\\:/\\- ]+[\\w](?!\\/N)))([ ]+[EA]+[ ]*[\\d]+)*)([\W]|$)', re.UNICODE)])
	        self.regexCep = re.compile(u'((.*?[\\D])|^)(?P<order>(CEP[\\\\/ :\\-\\.]{0,2})?[\\d]{2}[,\\.\\-]?[\\d]{3}(( \\- )|[\\-])?[\\d]{3})($|[\\D])')
	        self.regexComplementoBaseCorreios = re.compile(u'.*?(?P<order>(- ((D(E|O))|(AT[EÉ]))( RUA)?( KM)? [\d,]+([/]+[\d,]*)?( AO (FIM|((KM )[\d,]*([/]+[\d,]*)?)))?( - LADO (PAR|[IÍ]MPAR))?))')
	        self.regexCidade = re.compile(u'.*?[^\W_].*?[:\\\\/ ,\\–\\-\\.|;](?P<order>[^\W\d_]([^\W\d_]|[ ]|([^\W\d_][\\–\\-][^\W\d_]))+)[:\\\\/ ,\\–\\-\\.|;]*$', re.UNICODE);
	        ''' self.regexCidade = re.compile(u'.*?(?P<order>[^\W\d_]([^\W\d_]|[ ]|([^\W\d_][\\–\\-][^\W\d_]))+)[:\\\\/ ,\\–\\-\\.|;]*$', re.UNICODE);'''
	        ''' identificadores de dados secundários textuais, como bairro e edifício '''
	        self.identificadoresSecundariosTextuais = [u'RESIDENCIAL', u'RES.', u'SITIO', u'SÍTIO', u'SíTIO', u'CHáCARA', u'CHÁCARA', u'CHACARA', u'SETOR']
	        self.identificadoresSecundariosTextuaisRegex = []
	        for identificadorSecundario in self.identificadoresSecundariosTextuais:
	            self.identificadoresSecundariosTextuaisRegex.append(re.compile(u'.*?(?P<order>[ ,]+'+identificadorSecundario+u'[\\. ]+[\\w ]*)', re.UNICODE))
	        ''' identificadores que tem o numero antes do nome ex: 2° andar '''
	        self.identificadoresSecundariosInvertidosRE = []
	        self.identificadoresSecundariosInvertidosRE.append(['andar', re.compile(u'.*?(?P<order>[\\d]+[°º\\.\\? ]*AND(AR)?([\\. ,\\-]|$)+)')])
	        self.identificadoresSecundariosInvertidosRE.append(['subsolo', re.compile(u'.*?(?P<order>[\\d]+[°º\\. ]*SUB(SOLO)?([\\. ,\\-]|$)+)')])
	        self.identificadoresSecundariosInvertidosRE.append(['andar', re.compile(u'.{4,}?[\\\\/:\\–\\-,_\\(\\)]+.*?(?P<order>[\\d]+[°º](=?)([\\. ,\\-]|$)+)')])
	        ''' identificadores de Unidades Federativas, usados para saber se é uma rodovia '''
	        #self.unidadesFederativas = [u'BR', u'AC', u'AL', u'AP', u'AM', u'BA', u'CE', u'DF', u'ES', u'GO', u'MA', u'MT', u'MS', u'MG', u'PA', u'PB', u'PR', u'PE', u'PI', u'RJ', u'RN', u'RS', u'RO', u'RR', u'SC', u'SP', u'SE', u'TO']
	    # retorna uma instancia de LogradouroNumero
	    def separarLogradouroNumero(self, tipoDeLogradouro, enderecoCompleto, numero, complemento, cidade, uf, cep):
	        if (uf != None and self.regexDF.match(uf) != None):
	            enderecoCompleto = self.limpadorDeTexto.limparLogradouroDF_Preparacao(enderecoCompleto)
	        enderecoDividido = self.__separarCamposSecundarios(tipoDeLogradouro, enderecoCompleto, numero, complemento, cidade, uf, cep)        
	        if (enderecoDividido.numero == None):
	            fimDoLogradouro = self.limpadorDeTexto.encontrarFinalDoLogradouro(enderecoDividido)
	            if (fimDoLogradouro != None):
	                if (not(fimDoLogradouro.semNumero)):
	                    enderecoDividido.numero = enderecoDividido.logradouro[fimDoLogradouro.indiceFim:]
	                else:
	                    enderecoDividido.numero = None
	                enderecoDividido.logradouro = enderecoDividido.logradouro[:fimDoLogradouro.indiceFim]
	            else:
	                if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) == None):
	                    if (enderecoDividido.complemento != None and self.iniciaComNumeroRegex.match(enderecoDividido.complemento)):
	                        enderecoDividido.numero = enderecoDividido.complemento;
	        enderecoDividido.logradouro = self.limpadorDeTexto.limparLogradouro(enderecoDividido.logradouro)
	        if (enderecoDividido.numero != None):
	            if (isinstance(enderecoDividido.numero, (int,long))):
	                enderecoDividido.numero = self.limpadorDeTexto.limparNumero(str(enderecoDividido.numero), False)
	            else:
	                enderecoDividido.numero = self.limpadorDeTexto.limparNumero(enderecoDividido.numero, False)
	            if (enderecoDividido.numero != None and self.regexZeros.match(enderecoDividido.numero)):
	                enderecoDividido.numero = None
			#remove caracteres indesejaveis ao início do logradouro
	        enderecoDividido.logradouro = re.sub(u'^[/\\\\\.:\\-, "\']+', '', enderecoDividido.logradouro)
			#remove caracteres indesejaveis ao final do logradouro
	        enderecoDividido.logradouro = re.sub(u'[\./\\\\:\\-, "\']*$', '', enderecoDividido.logradouro)
	        if (enderecoDividido.tipoDeLogradouro != None):
	            enderecoDividido.logradouro = (enderecoDividido.tipoDeLogradouro.upper() + ' ' + enderecoDividido.logradouro).strip()
	        enderecoDividido.logradouro = self.limpadorDeTexto.removerAcentos(enderecoDividido.logradouro)
	        ''' Brasilia - Se sobrar no nome do logradouro apenas número, é porque o número é um numero no final da string e deve ser um lixo. '''
	        ''' Ex: QUADRA 01 LT 300/320 retorna "/320" nesta etapa '''        
	        if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) != None):
	            if (enderecoDividido.logradouro != None and self.diferenteDeNumeros.match(enderecoDividido.logradouro) != None):
	                enderecoDividido.logradouro = "";
	        enderecoDividido.tipoDeLogradouro  = self.limpadorDeTexto.removerAcentos(enderecoDividido.tipoDeLogradouro)
	        enderecoDividido.cidade = self.limpadorDeTexto.removerAcentos(enderecoDividido.cidade)
	        #cria complemento
	        enderecoDividido.complemento = ""
	        complementosPermitidos = [
	                                  "modulo",
	                                  "casaSemAbreviacao",
	                                  "loja",
	                                  "titulo",
	                                  "bairro",
	                                  "subsolo",
	                                  "caixaPostal",
	                                  "andar",
	                                  "apartamento",
	                                  "casa",
	                                  "sala"
	                                  ]
	        #complementos para enderecos nao-brasilia
	        if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) == None):
	            complementosPermitidosNaoDF = [
	                                           "setor",
	                                           "trecho",
	                                           "quadra",
	                                           "comercioLocal",
	                                           "areaEspecial",
	                                           "conjunto",
	                                           "bloco",
	                                           "lote"
	                                           ]
	            complementosPermitidos = complementosPermitidos + complementosPermitidosNaoDF
	        renomearComplementos = {}
	        renomearComplementos['casaSemAbreviacao'] = 'casa'
	        renomearComplementos['comercioLocal'] = 'comercio local'
	        renomearComplementos['areaEspecial'] = 'area especial'
	        renomearComplementos['caixaPostal'] = 'caixa postal'
	        for chaveComplemento, valorComplemento in vars(enderecoDividido).iteritems():
	            if chaveComplemento in complementosPermitidos:
	                if valorComplemento is not None:
	                    chaveComplementoFinal = chaveComplemento
	                    if chaveComplemento in renomearComplementos.keys():
	                        chaveComplementoFinal = renomearComplementos[chaveComplemento]
	                    enderecoDividido.complemento += u" {0} {1}".format(chaveComplementoFinal, valorComplemento)
	        if enderecoDividido.complemento == "":
	            enderecoDividido.complemento = None
	        else:
	            enderecoDividido.complemento = enderecoDividido.complemento.strip().upper()
	        if enderecoDividido.cidade != None:
	            enderecoDividido.cidade = enderecoDividido.cidade.strip().upper()
	        return enderecoDividido
	    def __separarCamposSecundarios(self, tipoDeLogradouro, endereco, numero, complemento, cidade, uf, cep):
	        if (uf != None):
	            uf = uf.upper().strip()
	        if (cidade != None):
	            cidade = cidade.strip()
	        if (numero != None and numero != '' and isinstance(numero, basestring)):
	            numero = numero.strip()
	        enderecoDividido = logradouro_numero.LogradouroNumero(None, None, cidade, uf)
	        enderecoDividido.inputLimpo = endereco
	        if (tipoDeLogradouro != None):
	            enderecoDividido.tipoDeLogradouro = tipoDeLogradouro.strip().upper()
	        if (numero != None and numero != '' and numero != 0 and numero != "0"):
	            if (isinstance(numero, float)):
	                numero = int(numero)
	            if (isinstance(numero, int)):
	                numero = str(numero)
	            enderecoDividido.numero = self.limpadorDeTexto.limparNumero(numero, False)
	        enderecoDividido.logradouro = '';
	        precisaTerNome = True;
	        enderecoOriginal = None;
	        primeiroEncontrado = None
	        if (cep != None):
	            cep = self.limpadorDeTexto.limparCep(cep)
	            match = self.regexCep.match(str(cep))
	            if (match != None):
	                valor = match.group('order')
	                if (valor != None and  valor != ''):
	                    enderecoDividido.cep = valor
	        if (endereco != None and endereco != ''):
	            enderecoMaiusculo = endereco.upper()
	            if (enderecoDividido.tipoDeLogradouro == None or enderecoDividido.tipoDeLogradouro == ''):
	                tipoDeLogradouroResposta = self.localizadorTipoDeLogradouro.encontrarTipoDeLogradouroNoComeco(enderecoMaiusculo, uf)
	                # limpa o tipo de logradouro caso ele exista
	                if (tipoDeLogradouroResposta != None and tipoDeLogradouroResposta.tipoDeLogradouroEncontrado != None):
	                    endereco = endereco[tipoDeLogradouroResposta.indiceFim:]
	                    # endereco = re.sub(u'^[/\\\\\.:\\-, "\']+', '', endereco)
	                    enderecoMaiusculo = endereco.upper()
	                    enderecoDividido.tipoDeLogradouro = tipoDeLogradouroResposta.tipoDeLogradouro.tipoDeLogradouro
	                    precisaTerNome = tipoDeLogradouroResposta.tipoDeLogradouro.logradouroPrecisaTerNome
	                else:
	                    ''' inverter endereços escritos com 'carlos gomes, avenida' '''
	                    if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) == None):
	                        tipoDeLogradouroResposta = self.localizadorTipoDeLogradouro.encontrarTipoDeLogradouroAposVirgula(enderecoMaiusculo)
	                        if (tipoDeLogradouroResposta != None and tipoDeLogradouroResposta.tipoDeLogradouroEncontrado != None):
	                            endereco = endereco[tipoDeLogradouroResposta.indiceInicio:]+' '+endereco[:tipoDeLogradouroResposta.indiceInicio]
	                            enderecoMaiusculo = endereco.upper()
	            else:
	                ''' ajuste para o caso de se ter "RUA" no campo tipo e "RUA ALBERTO DAMASTOR" no campo nome '''
	                if (enderecoMaiusculo.startswith(enderecoDividido.tipoDeLogradouro.upper())):
	                    endereco = endereco[len(enderecoDividido.tipoDeLogradouro):]
	                    enderecoMaiusculo = endereco.upper()
	            # print "endereco -5: ", enderecoDividido.tipoDeLogradouro
	            ''' Encontra CEP '''
	            if (enderecoDividido.cep == None or enderecoDividido.cep == ''):
	                match = self.regexCep.match(enderecoMaiusculo)
	                if (match != None):
	                    valor = match.group('order')
	                    if (valor != None and  valor != ''):
	                        if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                            primeiroEncontrado = match.start('order')
	                        enderecoDividido.cep = valor
	                        if match.end('order') < len(endereco):
	                            endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                        else:
	                            endereco = endereco[:match.start('order')]
	                        enderecoMaiusculo = endereco.upper()
	            ''' encontra estado '''
	            if (enderecoDividido.uf == None or enderecoDividido.uf == '' or enderecoDividido.uf == 'NULL'):
	                match = self.regexUfSigla.match(enderecoMaiusculo)
	                if (match != None):
	                    if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                        primeiroEncontrado = match.start('order')
	                    enderecoDividido.uf = match.group('order')
	                    endereco = endereco[:match.start('order')]
	                    enderecoMaiusculo = endereco.upper()
	                else:
	                    match = self.regexUfCompletoA.match(enderecoMaiusculo)
	                    match = match if match != None else self.regexUfCompletoB.match(enderecoMaiusculo)
	                    match = match if match != None else self.regexUfCompletoC.match(enderecoMaiusculo)
	                    if (match != None):
	                        dicionarioEncontrados = match.groupdict(None)
	                        for encontrado in dicionarioEncontrados:
	                            if (dicionarioEncontrados[encontrado] != None):
	                                if (primeiroEncontrado == None or primeiroEncontrado > match.start(encontrado)):
	                                    primeiroEncontrado = match.start(encontrado)
	                                enderecoDividido.uf = unicode(encontrado)
	                                endereco = endereco[:match.start(encontrado)]
	                                enderecoMaiusculo = endereco.upper()
	            else:
	                match = self.regexUfCompletoA.match(enderecoDividido.uf)
	                match = match if match != None else self.regexUfCompletoB.match(enderecoDividido.uf)
	                match = match if match != None else self.regexUfCompletoC.match(enderecoDividido.uf)
	                if (match != None):
	                    dicionarioEncontrados = match.groupdict(None)
	                    for encontrado in dicionarioEncontrados:
	                        if (dicionarioEncontrados[encontrado] != None):
	                            enderecoDividido.uf = unicode(encontrado)
	                else:
	                    enderecoDividido.uf = enderecoDividido.uf[:2]
	            ''' encontra cidade '''
	            if ((enderecoDividido.cidade == None or enderecoDividido.cidade == '' or enderecoDividido.cidade == 'NULL') and enderecoDividido.uf != None and uf == None):
	                match = self.regexCidade.match(enderecoMaiusculo)
	                if (match != None):
	                    if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                        primeiroEncontrado = match.start('order')
	                    enderecoDividido.cidade = self.limpadorDeTexto.limparLogradouro(endereco[match.start('order'):match.end('order')])
	                    if match.end('order') < len(endereco):
	                        endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                    else:
	                        endereco = endereco[:match.start('order')]
	                    enderecoMaiusculo = endereco.upper()
	            if (complemento != None and complemento != '' and complemento.upper() != 'NULL'):
	                inicioComplemento = len(endereco)
	                endereco = endereco + u' / ' + complemento
	            else:
	                inicioComplemento = None
	            enderecoMaiusculo = endereco.upper()
	            # print "endereco -3: ", enderecoDividido.tipoDeLogradouro
	            ''' remove sujeira da base do DNE '''
	            #remover dados complementares de endereço que vem da base de CEP dos correios
	            match = self.regexComplementoBaseCorreios.match(enderecoMaiusculo)
	            if (match != None):
	                if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                    primeiroEncontrado = match.start('order')
	                if match.end('order') < len(endereco):
	                    endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                else:
	                    endereco = endereco[:match.start('order')]
	                enderecoMaiusculo = endereco.upper()
	            # print "endereco -2A: ", enderecoMaiusculo
	            ''' encontra e remove complementos '''
	            for identificadorSecundario in self.identificadoresSecundariosRE:
	                if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) != None and identificadorSecundario[0] == 'casa'):
	                    continue;
	                match = identificadorSecundario[1].match(enderecoMaiusculo)
	                # print ' - ',identificadorSecundario[0]
	                if (match != None):
	                    if ((enderecoDividido.tipoDeLogradouro == 'RODOVIA' or enderecoDividido.tipoDeLogradouro == 'ESTRADA') and match.start('order') <= 3):
	                        continue;
	                    # print match.group(0), match.group(1);
	                    valor = self.limpadorDeTexto.limparNumeroLetra(match.group('order'), False)
	                    # print valor;
	                    if (valor != None and  valor != ''):
	                        if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                            primeiroEncontrado = match.start('order')
	                        if (identificadorSecundario[0] == 'kilometro'):
	                            try:
	                               valor = float(valor.replace(',', '.'))
	                            except ValueError:
	                               continue;
	                        setattr(enderecoDividido, identificadorSecundario[0], valor)
	                        if match.end('order') < len(endereco):
	                            endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                        else:
	                            endereco = endereco[:match.start('order')]
	                        enderecoMaiusculo = endereco.upper()
	            # print "endereco -2B: ", enderecoMaiusculo
	            ''' encontra e remove complementos com o numero antes do identificador
	                ex: 2º andar '''
	            for identificadorSecundario in self.identificadoresSecundariosInvertidosRE:
	                match = identificadorSecundario[1].match(enderecoMaiusculo)
	                if (match != None):
	                    if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                        primeiroEncontrado = match.start('order')
	                    valor = self.limpadorDeTexto.limparNumero(match.group('order'), True)
	#                    print match.group('order') + u': ' + unicode(valor);
	                    setattr(enderecoDividido, identificadorSecundario[0], valor)
	                    if match.end('order') < len(endereco):
	                        endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                    else:
	                        endereco = endereco[:match.start('order')]
	                    enderecoMaiusculo = endereco.upper()
	            # print "endereco -1: ", enderecoMaiusculo
	            ''' encontra numeração do logradouro por separador 
				    ex: nº 10
	                apenas para enderecos nao-Brasilia '''
	            if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) == None):
	                if (enderecoDividido.numero == None or enderecoDividido.numero == ''):
	                    # print "endereco: ", enderecoMaiusculo
	                    for separadorDeNumeroRegex in self.separadoresDeNumeroRegex:
	                        match = separadorDeNumeroRegex.match(enderecoMaiusculo)
	                        if (match != None):
	                            # print "achou separador"
	    #                        print 'Start:', match.start('order')
	                            if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                                primeiroEncontrado = match.start('order')
	                            numero = self.limpadorDeTexto.limparNumero(match.group('order'), False)
	    #                        print match.group('order') + u': ' + unicode(numero);
	                            enderecoDividido.numero = numero
	                            if match.end('order') < len(endereco):
	                                endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                            else:
	                                endereco = endereco[:match.start('order')]
	                            enderecoMaiusculo = endereco.upper()
	                            break
	            ''' remove marcadores de numeração remanescentes por erro de falso positivo para primeira rua e primeira avenida 
				    ex: nº conjunto solares nº 1 rua teste nº 1
					isso poderia dar falso positivo para primeira rua'''
	            if (enderecoDividido.numero != None):
	                for separadorDeNumeroRegex in self.separadoresDeNumeroRegex:
	                    match = separadorDeNumeroRegex.match(enderecoMaiusculo)
	                    if (match != None):
	                        if match.end('order') < len(endereco):
	                            endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                        else:
	                            endereco = endereco[:match.start('order')]
	                        enderecoMaiusculo = endereco.upper()
	                        break
	            ''' encontra numeração do logradouro por separador dentro do endereço original, caso não tenha sido encontrada no limpo
				    ex: nº 10 Rua beijamin franklin '''
	            if (enderecoOriginal != None and enderecoDividido.numero == None or enderecoDividido.numero == ''):
	                for separadorDeNumeroRegex in self.separadoresDeNumeroRegex:
	                    match = separadorDeNumeroRegex.match(enderecoOriginal.upper())
	                    if (match != None):
	#                        print 'Start:', match.start('order')
	                        if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                            primeiroEncontrado = match.start('order')
	                        numero = self.limpadorDeTexto.limparNumero(match.group('order'), False)
	#                        print match.group('order') + u': ' + unicode(numero);
	                        enderecoDividido.numero = numero
	                        break	
	            # print "endereco -1A: ", enderecoDividido.tipoDeLogradouro
				#tenta novamente achar o tipo de logradouro
	            if (enderecoDividido.tipoDeLogradouro == None or enderecoDividido.tipoDeLogradouro == ''):
	                endereco = endereco.strip()
	                enderecoMaiusculo = endereco.upper()
	                #print 'endereco:', endereco
	                tipoDeLogradouroResposta = self.localizadorTipoDeLogradouro.encontrarTipoDeLogradouroNoComeco(enderecoMaiusculo, enderecoDividido.uf)
	                '''
	                # gambiarra? remover? TODO: Checar se isto é necessário
	                # Resp: Para Brasilia essa regra não se aplica. Ex: QS 01 RUA 212
	                # Porém, para não quebrar testes anteriores de arruamento não-Brasília, inclui esta condição por DF
	                '''
	                if (tipoDeLogradouroResposta == None):
	                        if (enderecoDividido.uf != None and self.regexDF.match(enderecoDividido.uf) == None):
	                            tipoDeLogradouroResposta = self.localizadorTipoDeLogradouro.encontrarTipoDeLogradouroIndependenteDoLugar(enderecoMaiusculo)
	                # limpa o tipo de logradouro caso ele exista
	                if (tipoDeLogradouroResposta != None):
	                    if (tipoDeLogradouroResposta.indiceFim != None):
	                        enderecoOriginal = endereco
	                        endereco = endereco[tipoDeLogradouroResposta.indiceFim:]
	                        precisaTerNome = tipoDeLogradouroResposta.tipoDeLogradouro.logradouroPrecisaTerNome
	                    enderecoDividido.tipoDeLogradouro = tipoDeLogradouroResposta.tipoDeLogradouro.tipoDeLogradouro
	            enderecoMaiusculo = endereco.upper()
	            # print "endereco -1B: ", enderecoDividido.tipoDeLogradouro
	            ''' encontra e remove separadores textuais de identificadores 
				    ex: edifício, sítio... '''
	            for identificadorSecundario in self.identificadoresSecundariosTextuaisRegex:
	                match = identificadorSecundario.match(enderecoMaiusculo)
	                if (match != None):
	                    if (primeiroEncontrado == None or primeiroEncontrado > match.start('order')):
	                        primeiroEncontrado = match.start('order')
	                    if match.end('order') < len(endereco):
	                        endereco = endereco[:match.start('order')]+endereco[match.end('order'):]
	                    else:
	                        endereco = endereco[:match.start('order')]
	                    enderecoMaiusculo = endereco.upper()
	            if (inicioComplemento != None and (primeiroEncontrado == None or (primeiroEncontrado == 0 and precisaTerNome) or primeiroEncontrado > inicioComplemento)):
	                primeiroEncontrado = inicioComplemento
	            if (primeiroEncontrado != None and (primeiroEncontrado > 0 or not(precisaTerNome))):
	#                print endereco[primeiroEncontrado:]
	                enderecoDividido.complemento = endereco[primeiroEncontrado:]
	                enderecoDividido.logradouro = endereco[:primeiroEncontrado]
	            else:
	                enderecoDividido.logradouro = endereco;
	            enderecoDividido.logradouro = enderecoDividido.logradouro.upper();
	            # print "LOG:", enderecoDividido.logradouro
	        if (enderecoDividido.cep != None and enderecoDividido.cep != ''):
	            enderecoDividido.cep = self.limpadorDeTexto.limparCep(str(enderecoDividido.cep))
	        return enderecoDividido


# ------------------------------ 
# CLASSES / PRINCIPAIS

class conector_data_cleansing():

	dir = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(os.path.join(dir, "services"))
	class ConectorDataCleansing(object):
	    def __init__(self):
	        self.regexDF = re.compile(u'.*?(?P<separador>((DF)|(D[IíÍ]ST(R([IíÍ]TO)?)? FED(ERAL)?)))')
	        self.pe = preparador_de_endereco.PreparadorDeEndereco()
	        self.me = montador_de_endereco.MontadorDeEndereco()
	    def normalizarEndereco(self, tipoDeLogradouro, enderecoCompleto, numero, complemento, cidade, uf, cep):
	        enderecoSeparado = self.pe.separarLogradouroNumero(tipoDeLogradouro, enderecoCompleto, numero, complemento, cidade, uf, cep)
	        # --
	        camposNormalizados = {}
	        camposNormalizados["Tipo"] = u''
	        camposNormalizados["Numero"] = u''
	        camposNormalizados["Endereco"] = u''
	        camposNormalizados["Logradouro"] = u''
	        camposNormalizados["Cidade"] = u''
	        camposNormalizados["Uf"] = u''
	        camposNormalizados["Cep"] = u''
	        camposNormalizados["Cep7"] = u''
	        camposNormalizados["Cep6"] = u''
	        camposNormalizados["Cep5"] = u''
	        camposNormalizados["CepNum"] = u''
	        camposNormalizados["RodoviaKm"] = u''
	        camposNormalizados["RodoviaM"] = u''    
	        camposNormalizados["Complemento"] = u''   
	        camposNormalizados["LogradouroSemTipo"] = u''            
	        # --
	        camposNormalizados["Tipo"] = enderecoSeparado.tipoDeLogradouro
	        if (enderecoSeparado.numero != None):
	            camposNormalizados["Numero"] = str(enderecoSeparado.numero)
	        camposNormalizados["Endereco"] = self.me.montarEndereco(enderecoSeparado)
	        if (enderecoSeparado.uf != None and self.regexDF.match(enderecoSeparado.uf) != None):
	            camposNormalizados["Logradouro"] = camposNormalizados["Endereco"]
	        else:
	            camposNormalizados["Logradouro"] = enderecoSeparado.logradouro
	        camposNormalizados["Cidade"] = enderecoSeparado.cidade
	        camposNormalizados["Uf"] = enderecoSeparado.uf
	        if (enderecoSeparado.cep != None and enderecoSeparado.cep != ''):
	            camposNormalizados["Cep"] = enderecoSeparado.cep
	            camposNormalizados["Cep7"] = enderecoSeparado.cep[:7]
	            camposNormalizados["Cep6"] = enderecoSeparado.cep[:6]
	            camposNormalizados["Cep5"] = enderecoSeparado.cep[:5]
	            campoNormalizadoCepNumTemp = u''
	            if (enderecoSeparado.uf != None and self.regexDF.match(enderecoSeparado.uf) != None):
	                if (enderecoSeparado.lote != None):
	                    campoNormalizadoCepNumTemp = enderecoSeparado.cep + u' LT ' + enderecoSeparado.lote;
	            elif (enderecoSeparado.numero != None):
	                campoNormalizadoCepNumTemp = enderecoSeparado.cep + u', ' + enderecoSeparado.numero;
	            if len(campoNormalizadoCepNumTemp) > 20:
	                campoNormalizadoCepNumTemp = u''
	            camposNormalizados["CepNum"] = campoNormalizadoCepNumTemp
	        if (enderecoSeparado.kilometro != None):
	            kilometro = str(int(enderecoSeparado.kilometro))
	            metro = str(int(enderecoSeparado.kilometro * 1000))
	            camposNormalizados["RodoviaKm"] = enderecoSeparado.logradouro + u', ' + kilometro
	            camposNormalizados["RodoviaM"] = enderecoSeparado.logradouro + u', ' + metro
	        if (enderecoSeparado.complemento != None):
	            camposNormalizados["Complemento"] = enderecoSeparado.complemento
	        if (camposNormalizados["Tipo"] != None):
	            camposNormalizados["LogradouroSemTipo"] = (camposNormalizados["Logradouro"][len(camposNormalizados["Tipo"]):]).strip()
	        else:
	            camposNormalizados["LogradouroSemTipo"] = camposNormalizados["Logradouro"]
	        return camposNormalizados
	# ----------------
	# ----------------
	# TESTE CONECTOR
	# ----------------
	# cdc = ConectorDataCleansing()
	# print cdc.normalizarEndereco(None, "CJ 3 QD 5 BL 2", None, None, "BRASILIA", "DISTRITO FEDERAL", None)
	# ----------------

