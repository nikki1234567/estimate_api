from flask import Flask, request, jsonify, make_response,redirect,url_for,render_template,session
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import pandas as pd
import pickle
import json
import re
# from pattern.en import suggest



app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

with open('configuration.txt') as json_file:
    config= json.load(json_file)

# with open('unmatchedlist.pickle', 'rb') as handle:
#     unmatchedlist = pickle.load(handle)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/success/<name>')
# @token_required

def success(name):
	df_relation = pd.read_csv(config['dataframe_paths']['relation'][1])
	default_f = pd.read_csv(config['dataframe_paths']['FeatureAddonlist'][1])
	with open('featuredictionary1.pickle', 'rb') as handle:
	    feature_dictionary = pickle.load(handle)
	wordpress_default = []
	# project_default = {'Push to staging':4,'Push to production':5,'QA':20,'Hosting and environment setup(local and production)':10,'Planning and analysis':10}
	project_default = config['project_default']
	for ind in default_f.index:
	    if default_f['WordPress Default'][ind]=='D':
	        wordpress_default.append(default_f['Featrues'][ind])
	        
	feature_list = [f for f in wordpress_default]
	c1_feat = df_relation['Feature'].tolist()
	c2_class = df_relation['Synonyms'].tolist()
	c3_features = df_relation['Actual_feature'].tolist()
	c2_class_split = {}
	index =0    
	for c in c2_class:
	    for x in c.split(','):
	        c2_class_split[x.lower().strip()]=index
	    index+=1
	ans=[]
	for tok in name.split(','):
		feature_list.append(tok)
	feature_keys = [x.lower() for x in feature_dictionary.keys()]
	def reduce_lengthening(text):
		pattern = re.compile(r"(.)\1{2,}")
		return pattern.sub(r"\1\1", text)

	# def correction(text):
	# 	word_wlf = reduce_lengthening(text) #calling function defined above
	    
	# 	correct_word = suggest(word_wlf) 
	# 	return correct_word

	def get_hours(fe):
	    flag=0
	    if fe.lower() in feature_keys:
	        return feature_dictionary[fe.lower()]

	        flag=1
	    else:
	        for fk in feature_keys:
	            keysplit = [y.strip() for y in fk.split(',')]
	            if fe.lower() in keysplit:
	                return feature_dictionary[fk]
	                # ans.append(feature_dictionary[fk])

	                flag=1
	                
	    if flag==1:
	        x=0
	     
	    
	    else:
	        if fe.lower() in c1_feat:
	            ind = c1_feat.index(fe.lower())
	            di = feature_dictionary[c3_features[ind].lower()]
	            return di
	            # ans.append(di)
	            
	        elif fe.lower() in c2_class_split.keys():
	            dic = c3_features[c2_class_split[fe.lower().strip()]] 
	            di = feature_dictionary[dic.lower().strip()]
	            return di
	            # ans.append(di)

	        else:
	            fe_splt = fe.lower().strip().split(' ')
	            possibilities=[]
	            itr1=0
	            for c1 in c1_feat:
	                c1_tok = c1.split(' ')
	                if len(fe_splt)==1:
	                    li_int = [value for value in fe_splt if value in c1_tok]
	                    if len(li_int)!=0:
	                        temp=feature_dictionary[c3_features[itr1].lower()]
	                        possibilities.append([c3_features[itr1],temp])
	                else:
	                    if c1_tok[0]==fe_splt[0]:
	                        temp=feature_dictionary[c3_features[itr1].lower()]
	                        possibilities.append([c3_features[itr1],temp])
	                    
	                itr1+=1
	            itr2=0
	            for c2 in c2_class_split.keys():
	                c2_tok = c2.split(' ')
	                if len(fe_splt)==1:
	                    li_int1 = [value for value in fe_splt if value in c2_tok]
	                    if len(li_int1)!=0:
	                        temp2 = feature_dictionary[c3_features[c2_class_split[c2]].lower()]
	                        possibilities.append([c3_features[c2_class_split[c2]],temp2])
	                else:
	                    if c2_tok[0]==fe_splt[0]:
	                        temp2 = feature_dictionary[c3_features[c2_class_split[c2]].lower()]
	                        possibilities.append([c3_features[c2_class_split[c2]],temp2])

	                itr2+=1
	            for c3 in c3_features:
	                keysplit1 = [y.strip() for y in c3.split(',')]
	                for ks in keysplit1:
	                    ks_tok = ks.split(' ')
	                    if len(fe_splt)==1:
	                        li_int2 = [value for value in fe_splt if value in ks_tok]
	                        if len(li_int2)!=0:
	                            temp3 = feature_dictionary[c3.lower()]
	                            possibilities.append([c3,temp3])
	                    else:
	                        if ks_tok[0]==fe_splt[0]:
	                             temp3 = feature_dictionary[c3.lower()]
	                             possibilities.append([c3,temp3])
	                         
	                        
	                
	                
	            return possibilities
	    

	for feat_now in feature_list:
	    ans.append(get_hours(feat_now))
	    
	ans_frame1 = list(zip(feature_list,ans))
	ans_frame=[]
	for it in ans_frame1:
	    temp_li =[]
	    temp_li.append(it[0])
	    temp_li.append(it[1])
	    ans_frame.append(temp_li)

	    


	um_now=[]
	for i in range(11,len(feature_list)):
	    if isinstance(ans_frame[i][1],list):
	        if len(ans_frame[i][1])==0:
	            um_now.append(ans_frame[i][0])
	  
	   
	for unmatched_feature in um_now:
	    corrected_word = []
	    for uf_token in unmatched_feature.split(' '):
	        corrected_word.append(reduce_lengthening(uf_token))
	    modified_word = ' '.join(corrected_word)
	    for entry in ans_frame:
	        if entry[0]==unmatched_feature:
	            entry[0]=modified_word
	            entry[1]=get_hours(modified_word)
	ans_dict = {}
	ans_dict['Total_hours']=0
	um=[]
	total_hours=0
	for i in range(11,len(feature_list)):
	    if isinstance(ans_frame[i][1],list):
	        if len(ans_frame[i][1])!=0:
	            s=0
	            for j in range(len(ans_frame[i][1])):
	                s+= ans_frame[i][1][j][1]
	            s=s/len(ans_frame[i][1])
	            ans_dict[ans_frame[i][0]] = round(s,2)   
	            # print(f'{ans_frame[i][0].ljust(60)}{round(s,2)}hrs')

	            
	            total_hours+=round(float(s),2)
	        else:
	            um.append(ans_frame[i])
	    else:
	        # print(f'{ans_frame[i][0].ljust(60)}{round(float(ans_frame[i][1]),2)}hrs')
	        ans_dict[ans_frame[i][0]] = round(float(ans_frame[i][1]),2)

	        total_hours+=round(float(ans_frame[i][1]),2)

	if len(um)!=0:        
	    # print('\n***************** Unmatched features ********************\n')

	    for entry in um:
	    	# unmatchedlist.append(entry)
	    	ans_dict[entry[0]] = '-'
	        # print(f'{entry[0].ljust(60)}-')
	# print('\n***************** Wordpress Default ********************\n')       
	for i in range(0,11):
		ans_dict[ans_frame[i][0]]=round(ans_frame[i][1],2)
	    # print(f'{ans_frame[i][0].ljust(60)}{round(ans_frame[i][1],2)}hrs')
		total_hours+=round(ans_frame[i][1],2)
	    
	# print('\n***************** Project Default ********************\n')
	total_hours1=0
	for k,v in project_default.items():
	    if k=='Push to staging':
	        val=max(0.5,round((v/100)*total_hours,2))
	        ans_dict[k]=val
	        # print(f'{k.ljust(60)}{val}hrs')
	        total_hours1+=val
	    elif k=='Push to production':
	        val = max(0.5,round((v/100)*total_hours,2))
	        ans_dict[k]=val
	        # print(f'{k.ljust(60)}{val}hrs')
	        total_hours1+=val
	    elif k=='QA':
	        val = max(1,round((v/100)*total_hours,2))
	        ans_dict[k]=val
	        # print(f'{k.ljust(60)}{val}hrs')
	        total_hours1+=val
	    elif k=='Hosting and environment setup(local and production)':
	        val = min(20,round((v/100)*total_hours,2))
	        ans_dict[k]=val
	        # print(f'{k.ljust(60)}{val}hrs')
	        total_hours1+=val
	    elif k=='Planning and analysis':
	        val = max(1,round((v/100)*total_hours,2))
	        ans_dict[k]=val
	        # print(f'{k.ljust(60)}{val}hrs')
	        total_hours1+=val


	ans_dict['Total_hours']=total_hours+total_hours1
	# with open('unmatchedlist.pickle', 'wb') as handle:
	# 	pickle.dump(unmatchedlist, handle, protocol=pickle.HIGHEST_PROTOCOL)
	return jsonify(ans_dict)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)



@app.route('/user', methods=['POST'])
def create_user():
    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user', methods=['GET'])
@token_required
def get_all_users():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/login',methods=['POST','GET'])

def login():
    
	error = None
	if request.method == 'POST':
		user = User.query.filter_by(name=request.form['username']).first()
		if not user:
			return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

		else:
			if check_password_hash(user.password, request.form['password']):
				session['username']=request.form['username']
				token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
				return jsonify({'token' : token.decode('UTF-8')})
			else:
				return make_response('Could not verify wrong username or password')
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('login'))



@app.route('/features',methods = ['POST', 'GET'])
@token_required
def features():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
    app.run(debug=True)

