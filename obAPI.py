import urllib2
import json
import ssl
import csv


OPEN_BRAVO_USERNAME = 'baysingersapi'
OPEN_BRAVO_PASSWORD = 'openbravo'
OPEN_BRAVO_SERVER = 'https://openbravo.baysingers.com'
OPEN_BRAVO_SOURCE = '%s/openbravo/org.openbravo.service.json.jsonrest' % OPEN_BRAVO_SERVER
OPEN_BRAVO_RESOURCES = [
    {'name': 'uOM', 'schema_name': 'UOMType', 'url': '%s/UOM/' % OPEN_BRAVO_SOURCE, },
    {'name': 'ProductCategory', 'schema_name': 'ProductCategoryType', 'url': '%s/ProductCategory/' % OPEN_BRAVO_SOURCE,
     'reference': 'ProductCategory', },
    {'name': 'ProductSubCategory', 'schema_name': 'palt_psubcatType', 'url': '%s/palt_psubcat/' % OPEN_BRAVO_SOURCE,
     'reference': 'palt_psubcat', },
    {'name': 'Product', 'schema_name': 'ProductType', 'url': '%s/Product/' % OPEN_BRAVO_SOURCE,
     'reference': 'Product', },
    {'name': 'PriceList', 'schema_name': 'PricingPriceListType', 'url': '%s/PricingPriceList/' % OPEN_BRAVO_SOURCE,
     'reference': 'PricingPriceList', },
    {'name': 'PriceListVersion', 'schema_name': 'PricingPriceListVersionType',
     'url': '%s/PricingPriceListVersion/' % OPEN_BRAVO_SOURCE, 'reference': 'PricingPriceListVersion', },
    {'name': 'ProductPrice', 'schema_name': 'PricingProductPriceType',
     'url': '%s/PricingProductPrice/' % OPEN_BRAVO_SOURCE, 'reference': 'PricingProductPrice', },
    {'name': 'BusinessPartner', 'schema_name': 'BusinessPartnerType', 'url': '%s/BusinessPartner/' % OPEN_BRAVO_SOURCE,
     'reference': 'BusinessPartner', },
    {'name': 'BusinessPartnerCategory', 'schema_name': 'BusinessPartnerCategoryType',
     'url': '%s/BusinessPartnerCategory/' % OPEN_BRAVO_SOURCE, 'reference': 'BusinessPartnerCategory', },
    {'name': 'ADUser', 'schema_name': 'ADUserType', 'url': '%s/ADUser/' % OPEN_BRAVO_SOURCE, 'reference': 'ADUser', },
    {'name': 'Location', 'schema_name': 'LocationType', 'url': '%s/Location/' % OPEN_BRAVO_SOURCE,
     'reference': 'Location', },
    {'name': 'BusinessPartnerLocation', 'schema_name': 'BusinessPartnerLocationType',
     'url': '%s/BusinessPartnerLocation/' % OPEN_BRAVO_SOURCE, 'reference': 'BusinessPartnerLocation', },
    {'name': 'Department', 'schema_name': 'palt_departmentType', 'url': '%s/palt_department/' % OPEN_BRAVO_SOURCE,
     'reference': 'palt_department', },
    {'name': 'AgencyAllowance', 'schema_name': 'palt_agency_allowanceType',
     'url': '%s/palt_agency_allowance/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_agency_allowance', },
    {'name': 'PurchaseMethod', 'schema_name': 'palt_purchasemethodType',
     'url': '%s/palt_purchasemethod/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_purchasemethod', },
    {'name': 'Alteration', 'schema_name': 'palt_alterationType', 'url': '%s/palt_alteration/' % OPEN_BRAVO_SOURCE,
     'reference': 'palt_alteration', },
    {'name': 'Order', 'schema_name': 'OrderType', 'url': '%s/Order/' % OPEN_BRAVO_SOURCE, 'reference': 'Order', },
    {'name': 'OrderLine', 'schema_name': 'OrderLineType', 'url': '%s/OrderLine/' % OPEN_BRAVO_SOURCE,
     'reference': 'OrderLine', },
    {'name': 'Institution', 'schema_name': 'palt_bpinstitutionType',
     'url': '%s/palt_bpinstitution/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_bpinstitution', },
    {'name': 'Variant', 'schema_name': 'ProdVar_MasterDataType', 'url': '%s/ProdVar_MasterData/' % OPEN_BRAVO_SOURCE,
     'reference': 'ProdVar_MasterData', },
    {'name': 'VariantOption', 'schema_name': 'PRODVAR_optnameType', 'url': '%s/PRODVAR_optname/' % OPEN_BRAVO_SOURCE,
     'reference': 'PRODVAR_optname', },
    {'name': 'VariantValue', 'schema_name': 'PRODVAR_optvalueType', 'url': '%s/PRODVAR_optvalue/' % OPEN_BRAVO_SOURCE,
     'reference': 'PRODVAR_optvalue', },
    {'name': 'AlterationSet', 'schema_name': 'palt_alterationsetType',
     'url': '%s/palt_alterationset/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_alterationset', },
    {'name': 'AlterationSetInstance', 'schema_name': 'palt_alterationsetinstanceType',
     'url': '%s/palt_alterationsetinstance/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_alterationsetinstance', },
    {'name': 'ClassType', 'schema_name': 'palt_classType', 'url': '%s/palt_class/' % OPEN_BRAVO_SOURCE,
     'reference': 'palt_class', },
    {'name': 'BusinessPartnerAlterationSpect', 'schema_name': 'palt_bpaltspecType',
     'url': '%s/palt_bpaltspec/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_bpaltspec', },
    {'name': 'AlterationBomline', 'schema_name': 'palt_alteration_bomlineType',
     'url': '%s/palt_alteration_bomline/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_alteration_bomline', },
    {'name': 'AlterationValue', 'schema_name': 'palt_alterationvalueType',
     'url': '%s/palt_alterationvalue/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_alterationvalue', },
    {'name': 'AlterationUse', 'schema_name': 'palt_alterationuseType',
     'url': '%s/palt_alterationuse/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_alterationuse', },
    {'name': 'AlterationInstance', 'schema_name': 'PALT_ALTERATIONINSTANCEType',
     'url': '%s/PALT_ALTERATIONINSTANCE/' % OPEN_BRAVO_SOURCE, 'reference': 'PALT_ALTERATIONINSTANCE', },
    {'name': 'PaymentPlanPaymentMethod', 'schema_name': 'FIN_PaymentMethodType',
     'url': '%s/FIN_PaymentMethod/' % OPEN_BRAVO_SOURCE, 'reference': 'FIN_PaymentMethod', },
    {'name': 'PaymentPlan', 'schema_name': 'FIN_Payment_Sched_Inv_VType',
     'url': '%s/FIN_Payment_Sched_Inv_V/' % OPEN_BRAVO_SOURCE, 'reference': 'FIN_Payment_Sched_Inv_V', },
    {'name': 'PickingList', 'schema_name': 'OBWPL_pickinglistType', 'url': '%s/OBWPL_pickinglist/' % OPEN_BRAVO_SOURCE,
     'reference': 'OBWPL_pickinglist', },
    {'name': 'OrderLineStatus', 'schema_name': 'palt_orderline_statusType',
     'url': '%s/palt_orderline_status/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_orderline_status', },
    {'name': 'ProductStyle', 'schema_name': 'PRODVAR_styleType', 'url': '%s/PRODVAR_style/' % OPEN_BRAVO_SOURCE,
     'reference': 'PRODVAR_style', },
    {'name': 'ProductStyleOption', 'schema_name': 'PRODVAR_styleoptType',
     'url': '%s/PRODVAR_styleopt/' % OPEN_BRAVO_SOURCE, 'reference': 'PRODVAR_styleopt', },
    {'name': 'BusinessPartnerProductList', 'schema_name': 'palt_bpprodlistType',
     'url': '%s/palt_bpprodlist/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_bpprodlist', },
    {'name': 'Locator', 'schema_name': 'LocatorType', 'url': '%s/Locator/' % OPEN_BRAVO_SOURCE,
     'reference': 'Locator', },
    {'name': 'InventoryTransaction', 'schema_name': 'MaterialMgmtMaterialTransactionType',
     'url': '%s/MaterialMgmtMaterialTransaction/' % OPEN_BRAVO_SOURCE,
     'reference': 'MaterialMgmtMaterialTransaction', },
    {'name': 'AlterationSpectProduct', 'schema_name': 'palt_bpprodlistType',
     'url': '%s/palt_bpprodlist/' % OPEN_BRAVO_SOURCE, 'reference': 'palt_bpprodlist', },
    {'name': 'Invoice', 'schema_name': 'InvoiceType', 'url': '%s/Invoice/' % OPEN_BRAVO_SOURCE,
     'reference': 'Invoice', },
    {'name': 'InvoiceLine', 'schema_name': 'InvoiceLineType', 'url': '%s/InvoiceLine/' % OPEN_BRAVO_SOURCE,
     'reference': 'InvoiceLine', },
    {'name': 'Region', 'schema_name': 'RegionType', 'url': '%s/Region/' % OPEN_BRAVO_SOURCE, 'reference': 'Region', },
    {'name': 'Promotion', 'schema_name': 'bays_promotionalType', 'url': '%s/bays_promotional/' % OPEN_BRAVO_SOURCE,
     'reference': 'Promotion', },
]


def full_sync():
    array = OPEN_BRAVO_RESOURCES
    for resource in array:
        url = resource.get('url') or None
        schema_name = resource.get('schema_name') or None
        name = resource.get('name') or None
        if url and schema_name and name:
            response = request_resource(url=url)
            print "full_sync name: %s - response null?: %s" % (name, response is None)
            saveData(data=response, name=name)


def request_resource(url=None):
    response_data = {}
    print "request_resource --> url: {}".format(url)
    if url:
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            p = urllib2.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, url, OPEN_BRAVO_USERNAME, OPEN_BRAVO_PASSWORD)
            handler = urllib2.HTTPBasicAuthHandler(p)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            response = urllib2.urlopen(url)
            response_data = json.loads(response.read())
        except Exception, e:
            print "request_resource Error: %s" % e
    return response_data


def saveData(data=None, name=None):
    if data is not None and name is not None and name.strip():
        filename = "sync/%s.json" % name
        try:
            with open(filename, 'wb') as fp:
                json.dump(data, fp)
        except Exception, e:
            print "saveData Error: %s" % e


def saveSQL(data=None, name=None):
    if data is not None and name is not None and name.strip():
        filename = "syncPushSQL/%s.sql" % name
        try:
            dataFile = open(filename, 'wb')
            for row in data:
                dataString = row.encode('ascii', 'ignore')
                dataFile.write(dataString)
            dataFile.close()
        except Exception, e:
            pass


def readJSONData(name=None):
    data = None
    if name is not None and name.strip():
        filename = "sync/%s.json" % name
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
            if data is not None and 'response' in data.keys():
                data = data.get('response') or None
            if data is not None and 'data' in data.keys():
                data = data.get('data') or None
        except Exception, e:
            print "readJSONData - Exception: {}".format(e)
    return data


def generateCSV():
    array = OPEN_BRAVO_RESOURCES
    for resource in array:
        url = resource.get('url') or None
        schema_name = resource.get('schema_name') or None
        name = resource.get('name') or None
        definition = load_definition(name=name)
        if definition is not None:
            headers = [definition.get(key) for key in definition.keys()]
            file_path = 'csv/{}.csv'.format(name)
            with open(file_path, 'wb') as file:
                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL, dialect='excel')
                writer.writerows([headers])
                obData = readJSONData(name=name)
                if obData is not None:
                    rows = []
                    for d in obData:
                        row = [d.get(key, 'NULL').encode('ascii', 'ignore').strip()
                               if isinstance(d.get(key, 'NULL'), basestring)
                               else d.get(key, '') for key in definition]
                        rows.append(row)
                    writer.writerows(rows)


def generateSQL():
    array = OPEN_BRAVO_RESOURCES
    for resource in array:
        url = resource.get('url') or None
        schema_name = resource.get('schema_name') or None
        name = resource.get('name') or None
        data = readFieldsRelation(name=name)
        print "generateSQL --> name: {} ".format(name)
        try:
            data = json.loads(data)
            data = normalizeTableFields(data=data, name=name)
        except Exception ,e:
            print "generateSQL -- Exception: {}".format(e)
#            traceback.print_exc(file=sys.stdout)
            data = None
#        print "generateSQL --> data: {} ".format(data)
        if data is not None:
            sql = []
            sql.append('COPY "openBravo_%s" ' % name.lower())
            fields = ['"%s"' % data.get(k) for k in data.keys() if data.get(k) is not None and data.get(k).strip()]
            fields = ",".join(fields)
            fields = '(%s)' % fields
            sql.append(fields)
            sql.append(' FROM stdin WITH(NULL \'NULL\' );')
            sql.append('\n')
            print "generateSQL -- readJSONData --> Begin"
            obData = readJSONData(name=name)
            print "CLASS : {}".format(obData.__class__)
            print "generateSQL -- readJSONData --> End"
            valuesArray = []
#            print "generateSQL --> obData: {} ".format(obData)
            if obData is not None:
                filename = "syncPushSQL/%s.sql" % name
                try:
                    dataFile = open(filename, 'wb')
                    print "generateSQL -- WRITING HEADER"
                    for row in sql:
                        dataString = row.encode('ascii', 'ignore')
                        dataFile.write(dataString)
                    first = True
                    sql = None
                    print "generateSQL -- WRITING DATA"
                    for d in obData:
                        values = [cleanData(data=d.get(k)) for k in data.keys()]
                        values = "\t".join(values)
                        if first:
                            first = False
                            dataString = "%s" % values.encode('ascii', 'ignore')
                        else:
                            dataString = "\n%s" % values.encode('ascii', 'ignore')
                        del values
                        dataFile.write(dataString)
                        del dataString
                    print "generateSQL -- WRITING TAIL"
                    for row in ["\n\\.\n"]:
                        dataString = row.encode('ascii', 'ignore')
                        dataFile.write(dataString)
                    dataFile.close()
                except Exception, e:
                    print "generateSQL -- Exception:{}".format(e)
            else:
                sql = []
                print "generateSQL name: %s , size: %s" % (name, len(sql))
                saveSQL(data=sql, name=name)


def normalizeTableFields(data=None, name=None):
    if data is not None and name is not None and name.strip():
        aux = {}
        DB_NAME = 'openBravo_{}'.format(name).upper()
        if DB_NAME in OB_DB_FIELDS.keys():
            db_fields = OB_DB_FIELDS.get(DB_NAME) or []
            for key in data.keys():
                fieldName = data.get(key) or None
                if fieldName is not None and fieldName.strip() and fieldName.upper() in db_fields:
                    aux.update({key: fieldName})
        data = aux
    return data


def cleanData(data=None):
    if data is None:
        return 'NULL'
    if isinstance(data, basestring) and len(data.strip()) == 0:
        return 'NULL'
    if data is not None and data.__class__ is unicode and data.strip():
        data = data.replace("'", "''")
        data = data.replace("\r", "\\r")
        data = data.replace("\t", "\\t")
        data = data.replace("\n", "\\n\\r\\n")
        data = data.strip()
    return "%s" % data


def readFieldsRelation(name=None):
    data = None
    if name is not None and name.strip():
        filename = "syncDefinition/%s.json" % name
        try:
            with open(filename, "r") as ins:
                array = []
                for line in ins:
                    array.append(line)
                data = "\r\n".join([l for l in array if l is not None and l.strip()])
        except:
            pass
    return data


def fetch_json(filename=None):
    data = {}
    if filename is not None and filename.strip():
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
        except Exception,e :
            pass
    return data


def load_definition(name=None):
    definition_str = readFieldsRelation(name=name)
    if definition_str is not None:
        return json.loads(definition_str)
    else:
        return None

OB_DB_FIELDS = fetch_json('syncDefinition/db_fields.json')

# full_sync()
# generateSQL()
generateCSV()