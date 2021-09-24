import streamlit as st 

import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns 

from scipy import interpolate

from mpl_toolkits.mplot3d import Axes3D
from numpy import loadtxt,argmax,mean,median
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy.signal import savgol_filter
import plotly.graph_objects as go
#Enter data processing parameters:
savgolWindow = 11
savgolPoly = 3
sigNoiseThresh = 3
asymThresh = 1
asymThreshD = 1
cutoff = 15 # cut off ends of dVdI which result in spurious maxima

st.markdown(""" # Automated Ic extraction from current and voltage data ( PPMS data ) """)
st.set_option('deprecation.showPyplotGlobalUse', False)
data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "dat"])
delimiter_choice = st.text_input("Enter the Delimiter: \\t for tab , for coma etc","\\t")

def main():

	st.subheader("Data Visualization")
	if data is not None:
		df = pd.read_csv(data,delimiter=delimiter_choice)
		st.write("First 5 data")
		st.dataframe(df.head())

		all_columns_names = df.columns.tolist()

	
		# Customizable Plot
		activities = ["Find-Ic","Visualise-Data"]

		choice = st.radio("Select Operation",activities)


		if choice == "Visualise-Data":

			
			type_of_plot = st.radio("Select Type of Plot",["area","bar","line","hist","box","kde"])
			selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)


			if st.button("Generate Plot"):
				st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

				# Plot By Streamlit
				if type_of_plot == 'area':
					cust_data = df[selected_columns_names]
					st.area_chart(cust_data)

				elif type_of_plot == 'bar':
					cust_data = df[selected_columns_names]
					st.bar_chart(cust_data)

				elif type_of_plot == 'line':
					cust_data = df[selected_columns_names]
					st.line_chart(cust_data)

				# Custom Plot 
				elif type_of_plot:
					cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
					st.write(cust_plot)
					st.pyplot()


		elif choice == "Find-Ic":
			Icolumn = st.selectbox("Select Columns that contains I data",all_columns_names)
			Vcolumn = st.selectbox("Select Columns that contains V data",all_columns_names)
			st.write("Plot list")
			c1 = st.checkbox("Show dV/dI")
			c2 = st.checkbox("Show Savgol filter of 0th order")
			c3 = st.checkbox("Show Savgol filter of 1st order")
			

			v = df[Icolumn]
			i = df[Vcolumn]
			dvdi=np.array(v.diff()/i.diff())
			didv = np.array(i.diff()/v.diff())
			# plt.close()
			# plt.plot(i,dvdi,label='dV/dI')
			#plt.plot(i,get_sma(dvdi),'r')
			sg = savgol_filter(dvdi,savgolWindow,savgolPoly)   # Savgol filter of 0th order derivative
			sg2 = 10*abs(savgol_filter(sg,savgolWindow,savgolPoly,deriv=1))  # Savgol filter of 1st order derivative
			# plt.plot(i,sg,color='yellow', linestyle='dashed', marker='.',label='Savgol filter of dV/dI (=SG)')
			# plt.plot(i,sg2,color='green', linestyle='dashed', marker='.',label='Savgol filter of dSG/dI')
			# plt.xlabel('I (mA)')
			# plt.ylabel('dV/dI (mΩ)')
			# plt.legend(loc="upper left")
			# plt.show()
			# Create traces
			fig = go.Figure()
			if c1:
				fig.add_trace(go.Scatter(x=i, y=dvdi,
								mode='lines+markers',
								name='dV/dI'))
			if c2: 
				fig.add_trace(go.Scatter(x=i, y=sg,
								mode='lines+markers',
								name='0th order Savgol filter'))
			if c3:
				fig.add_trace(go.Scatter(x=i, y=sg2,
								mode='lines+markers', name='1st order Savgol filter'))

			
			fig.update_layout(title='Data for dV/dI and d^2V/dI^2', autosize=True,
			width=1024, height=800)
			st.plotly_chart(fig)
			fig.show()
			I=i

			sg2L = np.array(sg2[cutoff:int(0.5*(len(sg2)-1))])   # split sg2 into two groups left (neg) and right (pos)
			sg2R = np.array(sg2[int(0.5*(len(sg2)-1)):(len(sg2)-cutoff)] )

			IL = np.array(I[cutoff:int(0.5*(len(sg2)-1))] )
			IR = np.array(I[int(0.5*(len(sg2)-1)):(len(sg2)-cutoff)] )

			L = abs(IL[np.nanargmax(sg2L)])
			R = abs(IR[np.nanargmax(sg2R)])
			print(L)
			print(R)

			Ic = 0.5*(R+L)  # take average of R and L
			st.write('Ic = ' + str(Ic*1e6) + ' uA')
			st.write('asymmetry ratio:')
			st.write(abs((L - R))/min(L,R))
			st.write('asymmetry difference:')
			st.write(abs(L-R))
	st.write()



if __name__ == '__main__':
	main()
